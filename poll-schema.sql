-- ============================================================
-- Poll / attendance schema — econ-lectures
-- Supabase project: dpntbrsorgbivmntwmod
-- Run in the Supabase SQL editor. Safe to re-run.
--
-- STEP 1 ONLY. Deliberately NON-BREAKING: every existing deck keeps
-- working exactly as it does today after this runs. Nothing here
-- changes poll_votes RLS, so poll-admin's Clear buttons still work.
-- ============================================================

-- ---------- 0. Look before you leap (run these first, read output) ----------
-- select tablename, rowsecurity from pg_tables where schemaname = 'public';
-- select schemaname, tablename, policyname, cmd, roles from pg_policies where schemaname = 'public';

-- ---------- 1. Votes: session namespacing ----------
-- session_key looks like '2026-09-23-am'. Decks stamp it on write and
-- filter on it when reading, so the AM section's votes can never appear
-- in the PM section. No clearing required, and history is preserved.
alter table public.poll_votes
  add column if not exists session_key text;

create index if not exists poll_votes_session_idx
  on public.poll_votes (session_key, poll_id);

-- One vote per student, per poll, per session. Existing rows have a NULL
-- session_key and NULLs are distinct in a unique index, so no backfill
-- conflict — the constraint only starts biting once decks write the column.
create unique index if not exists poll_votes_one_per_student
  on public.poll_votes (poll_id, voter_id, session_key);

-- ---------- 2. Identities: device -> NUID, WRITE-ONLY to the public key ----------
-- Append-only. Latest row per device_id is that device's current NUID.
-- Append-only means no UPDATE policy is needed, which is what keeps the
-- table unreadable (see the policy note below).
create table if not exists public.poll_identities (
  id         uuid        primary key default gen_random_uuid(),
  device_id  text        not null,
  nuid       text        not null,
  created_at timestamptz not null default now()
);

create index if not exists poll_identities_device_idx
  on public.poll_identities (device_id, created_at desc);

alter table public.poll_identities enable row level security;

drop policy if exists "anon may check in" on public.poll_identities;
create policy "anon may check in"
  on public.poll_identities
  for insert to anon
  with check (
    nuid ~ '^[0-9]{9}$'                    -- VERIFIED 2026-09-22 against live Canvas
    and length(device_id) between 8 and 64
  );

-- !! THE WHOLE POINT !!
-- No SELECT / UPDATE / DELETE policy for anon is created here, on purpose.
-- With RLS enabled and no read policy, the anon key that is published in
-- every deck can INSERT a check-in but can NEVER read a NUID back.
-- Only the service_role key — used by your local export script, never by
-- a browser — can read this table. Do not add a SELECT policy for anon.

-- CANVAS JOIN KEY (verified 2026-09-22 against courses 262183 / 262188):
--   Canvas sis_user_id == login_id == 9 digits + 1 trailing letter (e.g. 00#######x),
--   and the 9-digit core is exactly the NUID a student types.
--   => You CANNOT address students as sis_user_id:<nuid>; the trailing letter
--      is missing. The export script must pull the roster once and join on the
--      9-digit core, asserting the core is unique across the section.

-- ---------- 3. Poll windows: when a vote counts ----------
-- Semantics (poll.js): if NO window row exists for a session_key, windows are
-- not in use and voting is open. Once any poll is opened in that session, an
-- unopened poll is treated as closed. So forgetting to press Open cannot kill
-- a class, but deliberate use of windows still enforces presence.
create table if not exists public.poll_windows (
  poll_id     text        not null,
  session_key text        not null,
  opened_at   timestamptz not null default now(),
  closed_at   timestamptz,
  primary key (poll_id, session_key)
);

alter table public.poll_windows enable row level security;

drop policy if exists "anyone may read windows" on public.poll_windows;
create policy "anyone may read windows"
  on public.poll_windows for select to anon using (true);
-- No anon write policy: windows are opened only through the RPCs below.

-- ---------- 4. Instructor passphrase + open/close RPCs ----------
create table if not exists public.poll_secrets (
  k text primary key,
  v text not null
);
alter table public.poll_secrets enable row level security;
-- No policies at all => invisible and unwritable to the anon key.

-- Seed the passphrase ONCE (edit the value, then run this line):
-- insert into public.poll_secrets (k, v) values ('instructor', 'CHANGE-ME')
--   on conflict (k) do update set v = excluded.v;

create or replace function public.open_poll(p_poll_id text, p_session_key text, p_pass text)
returns void language plpgsql security definer set search_path = public as $$
begin
  if p_pass is distinct from (select v from poll_secrets where k = 'instructor') then
    raise exception 'not authorized';
  end if;
  insert into poll_windows (poll_id, session_key, opened_at, closed_at)
  values (p_poll_id, p_session_key, now(), null)
  on conflict (poll_id, session_key)
    do update set opened_at = now(), closed_at = null;
end $$;

create or replace function public.close_poll(p_poll_id text, p_session_key text, p_pass text)
returns void language plpgsql security definer set search_path = public as $$
begin
  if p_pass is distinct from (select v from poll_secrets where k = 'instructor') then
    raise exception 'not authorized';
  end if;
  update poll_windows set closed_at = now()
   where poll_id = p_poll_id and session_key = p_session_key;
end $$;

revoke all on function public.open_poll(text, text, text)  from public;
revoke all on function public.close_poll(text, text, text) from public;
grant execute on function public.open_poll(text, text, text)  to anon;
grant execute on function public.close_poll(text, text, text) to anon;

-- ============================================================
-- KNOWN GAP, not fixed here (see notes):
-- poll_votes has no RLS, so the published anon key can still DELETE every
-- vote in every course. Harmless-ish today and poll-admin depends on it.
-- Fix it only together with switching poll-admin to an RPC, or the Clear
-- buttons break mid-semester.
-- ============================================================
