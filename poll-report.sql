-- ============================================================
-- Reading a class meeting back out: NUID + what each student answered.
-- Run in the Supabase SQL editor, then Results -> Export -> CSV for Canvas.
--
-- WHY THIS LIVES HERE AND NOT IN THE BROWSER
-- poll_identities has RLS with an INSERT policy and no SELECT policy, so the
-- anon key published in every deck can write a NUID but can NEVER read one
-- back. Joining votes to NUIDs therefore only works somewhere that bypasses
-- RLS: this editor, or a local script holding the service_role key. That is
-- the whole privacy design, not an inconvenience -- do not "fix" it by adding
-- a SELECT policy for anon.
-- ============================================================

-- ---------- 1. Participation for one meeting ----------
-- Change the session_key. Format: YYYY-MM-DD-am | YYYY-MM-DD-pm.
with id as (                        -- latest NUID per device; the table is append-only
  select distinct on (device_id) device_id, nuid
    from public.poll_identities
   order by device_id, created_at desc
)
select
  coalesce(id.nuid, '(not checked in)') as nuid,
  count(*)                              as polls_answered,
  min(v.created_at)                     as first_response,
  max(v.created_at)                     as last_response,
  string_agg(v.poll_id || '=' || v.choice, ', ' order by v.created_at) as answers
from public.poll_votes v
left join id on id.device_id = v.voter_id
where v.session_key = '2026-09-23-am'
group by 1
order by 1;

-- ---------- 2. Per-question breakdown (how the class actually answered) ----------
-- select poll_id, choice, count(*) as n
--   from public.poll_votes
--  where session_key = '2026-09-23-am'
--  group by 1,2 order by 1,2;

-- ---------- 3. Who checked in but never voted ----------
-- with id as (select distinct on (device_id) device_id, nuid
--               from public.poll_identities order by device_id, created_at desc)
-- select id.nuid from id
--  where not exists (select 1 from public.poll_votes v
--                     where v.voter_id = id.device_id
--                       and v.session_key = '2026-09-23-am');

-- ---------- 4. Housekeeping ----------
-- ALWAYS clear windows after testing. Any row makes that session "windows in
-- use", which marks every poll WITHOUT a window closed -- including other
-- chapters' polls in the same class.
-- delete from public.poll_windows;

-- CANVAS JOIN: sis_user_id is the 9-digit NUID plus a trailing letter, so
-- sis_user_id:<nuid> 404s. Pull the roster and join on the 9-digit core.

-- ============================================================
-- TODAY, 2026-09-23 — the 08:00 ECON 2316 meeting
--
-- Two things make this day special; later days need neither.
--
-- 1. session_key became course-scoped at 12:47 today (poll.js 8b0b12a).
--    Everything BEFORE that ran under the bare key '2026-09-23-am', which the
--    09:15 ECON 3916 class also wrote to. So this query filters on poll_id as
--    well -- without that you would count 3916 students as 2316 attendance.
--    From tomorrow the key is e.g. '2026-09-24-am-econ2316' and the poll_id
--    filter is unnecessary.
--
-- 2. ch04-survey-utility-* is the coffee/boba slider and is ANONYMOUS by
--    design -- its voter_id is student-chosen initials, not a device, and the
--    speaker notes tell students to use letters that are NOT their initials.
--    It is excluded here and must not be used for attendance.
-- ============================================================
with id as (
  select distinct on (device_id) device_id, nuid
    from public.poll_identities
   order by device_id, created_at desc
)
select
  coalesce(id.nuid, '(no check-in)')    as nuid,
  count(*)                              as answers,
  min(v.created_at)                     as first_seen,
  max(v.created_at)                     as last_seen,
  string_agg(v.poll_id || '=' || v.choice, ', ' order by v.created_at) as detail
from public.poll_votes v
left join id on id.device_id = v.voter_id
where v.session_key = '2026-09-23-am'
  and v.poll_id like '%econ2316%'      -- excludes the 3916 class AND the anonymous survey
group by 1
order by (id.nuid is null), 1;

-- How many of the 33 devices actually checked in? Run this to see the split
-- before you grade -- a student who pressed Cancel votes but earns no credit.
-- select count(*) filter (where id.nuid is not null) as with_nuid,
--        count(*) filter (where id.nuid is null)     as anonymous
--   from (select distinct v.voter_id from public.poll_votes v
--          where v.session_key = '2026-09-23-am' and v.poll_id like '%econ2316%') v
--   left join (select distinct on (device_id) device_id, nuid
--                from public.poll_identities order by device_id, created_at desc) id
--     on id.device_id = v.voter_id;
