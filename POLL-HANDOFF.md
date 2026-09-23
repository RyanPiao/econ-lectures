# Poll + NUID attendance — handoff for ECON 3916 and ECON 5200, Topics 3 and 4

Written 2026-09-23 by the 2316 poll session. Everything below was verified
against the live site and the live database on that date, not assumed. Where I
could not verify something, it says so.

Scope of this note: `ch03-eda-the-art-and-ethics-of-visualization` (T3) and
`ch04-robust-statistics-robustness-in-a-skewed-world` (T4), in both `econ3916/`
and `econ5200/`. The same edit applies to every other deck in those courses.

---

## 1. What already exists, so you do not rebuild it

All of this is live and shared. **You do not need to touch any of it.**

| Thing | Where | State |
|---|---|---|
| `poll.js` | repo root | live, loaded via `<script src="../../poll.js">` |
| `poll-secret.js` | repo root | live; CCGate-encrypted Supabase secret |
| `auth.js` (`CCGate`) | repo root | unchanged, pre-existing |
| Supabase schema | `poll-schema.sql` | **already applied** |
| Read-out queries | `poll-report.sql` | ready to run |
| Passphrase rotation | `rotate.py` | ready; `--sql` re-prints the seed line |

The database has `poll_votes` (with `session_key`), `poll_identities`,
`poll_windows`, `poll_secrets`, and the `open_poll` / `close_poll` RPCs.
Nothing course-specific is in there — it is one shared backend.

**`poll_votes` is GLOBAL.** Poll ids must be unique across every deck in every
course. Both your courses already namespace correctly
(`ch03-econ5200-poll-1`, `ch04-econ3916-poll-2`, …), so you are fine. Do not
introduce a bare `poll-1`.

---

## 2. What each deck needs — four edits plus one tag

Verified 2026-09-23: all four anchors below are present and unique in
`econ3916/ch03`, `econ3916/ch04`, `econ5200/ch03`, `econ5200/ch04`, and the
standard poll block is present in all four. The same edit applies unchanged.

**(a) Load the shared script**, immediately before the inline poll `<script>`
(the one starting `(function(){ var SU="https://dpntbrsorgbivmntwmod...`):

```html
<script src="../../poll.js"></script>
```

**(b) Stamp the vote** — carries device id + session key:

```js
// from
sf("POST","poll_votes",{poll_id:pid,choice:ch,voter_id:VID})
// to
sf("POST","poll_votes",(window.Poll?Poll.stamp(pid,ch):{poll_id:pid,choice:ch,voter_id:VID}))
```

**(c) Filter results to this session** — stops the AM class seeing PM votes:

```js
// from
sf("GET","poll_votes?poll_id=eq."+pid+"&select=choice")
// to
sf("GET","poll_votes?poll_id=eq."+pid+"&select=choice"+(window.Poll?Poll.q():""))
```

**(d) Gate the click on check-in** — this is what collects the NUID:

```js
// from
o.addEventListener("click",function(){vote(pid,o.dataset.choice);})
// to
o.addEventListener("click",function(){var go=function(){vote(pid,o.dataset.choice);};
if(window.Poll){Poll.ready(pid,go);}else{go();}})
```

**(e) Gate the polling loop** — the egress fix, see §4:

```js
// from
setInterval(function(){fetchR(pid);},2000)
// to
setInterval(function(){
  if(document.hidden) return;
  var s = g.closest("section");
  if(s && !s.classList.contains("present")) return;
  fetchR(pid);
},2000)
```

Every call site is written `window.Poll ? new : old`, so if `poll.js` fails to
load the deck behaves exactly as it does today. That property is deliberate —
keep it in anything you add.

---

## 3. The gotcha that will cost you an afternoon

**Use `g.closest("section")`, never `document.querySelector("section.present")`.**

On a vertical stack the OUTER stack element also carries `.present` and comes
first in document order, so the querySelector version returns the stack — which
still contains the poll's grid. It then reads as "still on the poll" on every
sub-slide of that stack, including the answer slide.

`g` is the `.poll-grid` element from the deck's existing
`document.querySelectorAll(".poll-grid").forEach(function(g){…})` loop, so it is
already in scope at the call site. `closest()` walks UP and returns the
innermost ancestor section — the sub-slide, which is what you want.

Measured on `econ2316/ch04` poll-1 (grid two sections deep, parent
`class="stack present"`):

| | requests in 12 s |
|---|---|
| on the poll sub-slide | 2 |
| moved DOWN to the answer sub-slide (stack still `.present`) | 0 |

5200 Producer independently confirmed the same on `econ5200/ch03` poll-2.

**Related:** the results/answer sub-slide often carries `data-poll-id` on its
results chart. If you gate anything on "does this slide mention a poll", the
answer slide looks like the poll. Match `.poll-grid[data-poll-id]` specifically.

---

## 4. Egress — why the gate matters more than the interval

Each refresh is ~950 bytes on the wire (headers dominate; the body is 2 bytes).
Ungated, every deck refreshes every poll every 2 s forever, on screen or not.

- Ungated: ~**14.5 GB per semester** against a **5 GB** free-plan allowance.
  This is why the project sits at 103% and shows EXCEEDING USAGE LIMITS.
- Gated (polling only while the slide is up, ~3 min per poll):

| | 2 s | 5 s |
|---|---|---|
| 30 students, semester | 257 MB | 103 MB |
| 80 students, semester | 685 MB | 274 MB |

**Keep your 2 s.** The gate does ~98% of the work; the interval is not the
lever. A student's own chart refreshes immediately anyway — the vote POST
chains `.then(function(){ fetchR(pid); })` — so the interval only governs how
fast the *projected* tally catches up.

---

## 5. How a class actually runs

Two modes. Pick one deliberately.

**Without `?presenter`** — no voting windows are ever created, every poll
accepts votes all session, NUID + timestamp + answer still recorded. Simplest,
zero risk. Recommended for your first run.

**With `?presenter`** — arriving at a poll does NOT open it. Press `o`, or the
button in speaker view. Leaving the slide closes it after a 20 s grace so a
student mid-tap still lands.

The safety net: until you open your FIRST poll of a session there are no window
rows at all, and voting is open everywhere. Once you open one, every poll
*without* a window counts as closed. The speaker bar distinguishes these —
grey "open by default" versus green "VOTING OPEN".

**After any testing, clear the windows**, or the next class in that same
`session_key` finds every unopened poll closed:

```sql
delete from public.poll_windows;
```

---

## 6. Known bugs — do not rediscover these

1. **Advancing to a poll's own answer sub-slide does not close voting.**
   Leaving that answer slide does. So there is a window where the correct
   answer is on screen and voting is still live. Network trace shows the
   scheduler runs and GETs `poll_windows` but never issues `rpc/close_poll` on
   that one transition. Three hypotheses were each wrong; unresolved.
   **Workaround: press `o` when you reveal the answer.**

2. **The `o` key binding is UNVERIFIED end-to-end.** Browser automation here
   cannot deliver real keystrokes to the tab — a capture-phase probe saw zero
   keydown events. The function it calls is tested and works. Press it yourself
   once before relying on it.

3. `poll-secret.js` must be fetched with `cache: "no-store"`. A `<script src>`
   gets cached, so after a passphrase rotation the deck keeps the OLD payload
   and the correct passphrase can never decrypt it — silently, because the
   projector suppresses every message. Already fixed in `poll.js`; relevant if
   you write anything that loads it.

---

## 7. Reading the data back out

`poll_identities` has RLS with an INSERT policy and **no SELECT policy**, so the
anon key published in every deck can write a NUID but can never read one back.
That is the privacy design — do not "fix" it by adding a SELECT policy.

So the join only runs where RLS does not apply: the Supabase SQL editor, or a
local script with the service_role key. Use `poll-report.sql`, change the
`session_key` line, then **Results → Export → CSV**.

Output is one row per student: `nuid`, `polls_answered`, `first_response`,
`last_response`, `answers`.

**Not yet Canvas-ready.** Canvas gradebook import wants its own column layout,
and `sis_user_id` is the 9-digit NUID **plus a trailing letter**, so a raw NUID
will not match. You need a roster join. Nobody has built that exporter yet.

---

## 8. Repo discipline — three accidental publishes happened on 2026-09-23

Several sessions write to `~/econ-lectures` concurrently, and **every session
commits as `Ryan Piao <yirsung@gmail.com>`** — the author line can never tell
you who wrote a change. Path and commit-message prefix are the only signals.

- Never `git add -u` or `git add -A`. Stage explicit paths only.
- Check `git diff --cached --name-only` is empty **before** staging, as its own
  command — not printed in the same `&&` chain as the add, or you read the
  result after the commit has already gone.
- Stage and commit in ONE command with nothing between them that can fail
  (5200 Producer's rule, after a failed `&&` chain left files staged for three
  minutes and someone else committed them).

---

## 9. Two-folder rule — and it is currently broken for your T4 decks

Each deck normally lives in two places: the authoring copy under
`econ-lecture-material/<course>/` and `~/econ-lectures/`, which is the only one
that pushes. Both `index.html` and `presentation.html` must stay identical.

Verified 2026-09-23, and you should resolve this before editing:

- `econ3916` T3 and `econ5200` T3: authoring copy exists but **differs from the
  repo** (e.g. econ3916 ch03: repo 276757 B, authoring 250687 B, ~104 lines
  apart; repo is newer). Do not blindly copy either direction.
- `econ3916` T4 and `econ5200` T4: the authoring folder has
  **`presentation.html` but NO `index.html`**. The pair is already incomplete.

GitHub Pages serves `index.html`, not `presentation.html`. Sync and push both.

---

## 10. Before you finish: run the step-notes checker

`TA/teaching-improvement/tools/step_notes_check.py` (5200 Producer's) catches
speaker notes that can never render, in both forms — `data-notes` on the
fragment element, and `aside.notes` nested inside one. Exit 1 if anything is
unreachable.

```bash
python3 step_notes_check.py econ5200/ch03-*/index.html
```

Status on 2026-09-23 for the four decks in scope: **all 0 unreachable**
(econ3916 T3/T4, econ5200 T3/T4). `econ2316/ch04` has 7 and is being handled
separately.

A warning from my own mistake: I wrote a quick checker that looked only for
nested `aside.notes` and reported "zero across all 23 decks". It was a false
negative — 2316 uses the `data-notes` attribute form. A second homemade version
then over-reported 14 on `econ5200/ch03`, which their tool correctly says is 0.
**Use their checker, not a fresh regex.**
