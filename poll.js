/* ============================================================
   econ-lectures — shared poll identity / attendance layer
   Loaded by every deck as  <script src="../../poll.js"></script>

   Owns: device id, NUID check-in, session namespacing, voting
   windows. Does NOT own rendering — each deck keeps its own
   chart code and calls into this.

   SAFETY CONTRACT (matters, read before editing):
     * If this file fails to load, every deck still works — all
       call sites are written as  window.Poll ? new : old.
     * If poll-schema.sql has NOT been run yet, this degrades to
       exactly the old behaviour instead of erroring. It probes
       for the session_key column once and omits it if absent,
       and treats a missing poll_windows table as "open".
   ============================================================ */
(function () {
  "use strict";

  var SU = "https://dpntbrsorgbivmntwmod.supabase.co";
  var SK = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRwbnRicnNvcmdiaXZtbnR3bW9kIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU4NjY5NzksImV4cCI6MjA5MTQ0Mjk3OX0.7__ja5Sq2AB__iFXhj-CKZJ0l7SjUerf8mpGQlo2bxI";

  var K_DEVICE = "ec_device_id";
  var K_NUID   = "ec_nuid";
  var K_PASS   = "ec_poll_pass";

  var IS_FILE = (window.location.protocol === "file:");
  var qs      = new URLSearchParams(window.location.search);
  var INSTRUCTOR = qs.has("instructor");

  // Feature probes — resolved once, then cached for the session.
  var hasSessionKey = null;   // null = unknown, true/false once probed
  var windowCache   = {};     // pollId -> {open:bool, at:ms}

  /* ---------- tiny helpers ---------- */

  function ls(k, v) {
    try {
      if (v === undefined) return window.localStorage.getItem(k);
      window.localStorage.setItem(k, v);
      return v;
    } catch (e) { return null; }   // private mode / blocked storage
  }

  function sf(method, path, body) {
    var o = {
      method: method,
      headers: {
        "apikey": SK,
        "Authorization": "Bearer " + SK,
        "Content-Type": "application/json",
        "Cache-Control": "no-cache, no-store",
        "Pragma": "no-cache"
      }
    };
    if (body) o.body = JSON.stringify(body);
    return fetch(SU + "/rest/v1/" + path, o);
  }

  function rpc(fn, args) {
    return sf("POST", "rpc/" + fn, args);
  }

  /* ---------- identity ---------- */

  function deviceId() {
    var d = ls(K_DEVICE);
    if (!d) {
      d = "d_" + Math.random().toString(36).slice(2, 10) +
                 Math.random().toString(36).slice(2, 10);
      ls(K_DEVICE, d);
    }
    return d;
  }

  function nuid() {
    var n = ls(K_NUID);
    return (n && /^[0-9]{9}$/.test(n)) ? n : null;
  }

  function setNuid(n) {
    ls(K_NUID, n);
    // Best-effort: record the mapping server-side. The anon key can
    // write this but can never read it back (see poll-schema.sql).
    // A failure here must never block a student from voting.
    if (!IS_FILE) {
      sf("POST", "poll_identities", { device_id: deviceId(), nuid: n })
        .catch(function () {});
    }
    paintChip();
  }

  /* ---------- session key: 2026-09-23-am ---------- */

  function sessionKey() {
    var forced = qs.get("sec");                      // ?sec=am / ?sec=pm
    var now = new Date();
    var half = forced ? forced.toLowerCase()
                      : (now.getHours() < 12 ? "am" : "pm");
    var p = function (x) { return (x < 10 ? "0" : "") + x; };
    return now.getFullYear() + "-" + p(now.getMonth() + 1) + "-" +
           p(now.getDate()) + "-" + half;
  }

  /* ---------- session_key column probe ---------- */
  // Runs once. Until it resolves we behave as if the column is absent,
  // which is the old behaviour and always safe.

  function probeSessionKey() {
    if (IS_FILE) { hasSessionKey = false; return Promise.resolve(false); }
    return sf("GET", "poll_votes?select=session_key&limit=1")
      .then(function (r) { hasSessionKey = r.ok; return r.ok; })
      .catch(function () { hasSessionKey = false; return false; });
  }

  /* ---------- public: read filter + write payload ---------- */

  // Appended to a PostgREST select so a section only ever reads its own votes.
  function q() {
    return hasSessionKey ? "&session_key=eq." + encodeURIComponent(sessionKey()) : "";
  }

  function stamp(pollId, choice) {
    var row = { poll_id: pollId, choice: choice, voter_id: deviceId() };
    if (hasSessionKey) row.session_key = sessionKey();
    return row;
  }

  /* ---------- voting windows ---------- */
  // Fails OPEN: a missing table, a network blip or an un-run migration
  // must never stop a class from voting. Enforcement that actually counts
  // happens in the export, not here.

  function isOpen(pollId) {
    if (IS_FILE || !hasSessionKey) return Promise.resolve(true);
    var c = windowCache[pollId];
    if (c && (Date.now() - c.at) < 3000) return Promise.resolve(c.open);
    // Query every window for this SESSION, not just this poll. If the
    // instructor has not opened a single poll yet this session, windows are
    // simply not in use and voting stays open -- forgetting to press Open can
    // never silently kill a class. Once any poll has been opened this session,
    // windows are in use and an unopened poll is treated as closed.
    return sf("GET", "poll_windows?session_key=eq." + encodeURIComponent(sessionKey()) +
                     "&select=poll_id,opened_at,closed_at")
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (rows) {
        if (rows === null)  return true;          // table absent -> open
        if (!rows.length)   return true;          // windows unused today -> open
        var mine = rows.filter(function (w) { return w.poll_id === pollId; })[0];
        var open = !!mine && !!mine.opened_at && !mine.closed_at;
        windowCache[pollId] = { open: open, at: Date.now() };
        return open;
      })
      .catch(function () { return true; });
  }

  function openPoll(pollId)  { return windowRpc("open_poll", pollId); }
  function closePoll(pollId) { return windowRpc("close_poll", pollId); }

  function windowRpc(fn, pollId) {
    var pass = ls(K_PASS);
    if (!pass) {
      pass = window.prompt("Instructor passphrase (stored on this device only):");
      if (!pass) return Promise.resolve(false);
      ls(K_PASS, pass);
    }
    return rpc(fn, { p_poll_id: pollId, p_session_key: sessionKey(), p_pass: pass })
      .then(function (r) {
        if (!r.ok) { ls(K_PASS, ""); toast("Passphrase rejected — try again."); return false; }
        windowCache[pollId] = null;
        toast(fn === "open_poll" ? "Voting OPEN" : "Voting closed");
        return true;
      })
      .catch(function () { toast("Could not reach the server."); return false; });
  }

  /* ---------- check-in UI ---------- */

  function modal(onDone) {
    if (document.getElementById("ec-checkin")) return;
    var wrap = document.createElement("div");
    wrap.id = "ec-checkin";
    wrap.innerHTML =
      '<div class="ec-ci-card">' +
        '<h3>Check in</h3>' +
        '<p>Enter your <strong>9-digit NUID</strong> once. This device will remember it ' +
           'for every class for the rest of the term.</p>' +
        '<input id="ec-ci-input" inputmode="numeric" autocomplete="off" ' +
               'maxlength="9" placeholder="00#######">' +
        '<div id="ec-ci-err"></div>' +
        '<div class="ec-ci-row">' +
          '<button id="ec-ci-cancel" type="button">Cancel</button>' +
          '<button id="ec-ci-go" type="button">Check in</button>' +
        '</div>' +
        '<p class="ec-ci-skip">Cancel (or Esc) still records your vote in the class ' +
           'result \u2014 it just will not count toward your participation credit.</p>' +
      '</div>';
    document.body.appendChild(wrap);

    var input = wrap.querySelector("#ec-ci-input");
    var err   = wrap.querySelector("#ec-ci-err");

    // Reveal.js swallows keystrokes and will navigate slides while a student
    // types digits. This is mandatory, not defensive.
    ["keydown", "keypress", "keyup"].forEach(function (ev) {
      input.addEventListener(ev, function (e) { e.stopPropagation(); });
    });

    function close(ok) {
      wrap.remove();
      if (onDone) onDone(ok);
    }

    function submit() {
      var v = (input.value || "").replace(/[^0-9]/g, "");
      if (!/^[0-9]{9}$/.test(v)) {
        err.textContent = "That should be exactly 9 digits.";
        input.focus();
        return;
      }
      setNuid(v);
      close(true);
    }

    wrap.querySelector("#ec-ci-go").addEventListener("click", submit);
    wrap.querySelector("#ec-ci-cancel").addEventListener("click", function () { close(false); });
    input.addEventListener("keydown", function (e) {
      if (e.key === "Enter") submit();
      if (e.key === "Escape") close(false);
    });
    setTimeout(function () { input.focus(); }, 50);
  }

  function paintChip() {
    var chip = document.getElementById("ec-chip");
    var n = nuid();
    if (!n) { if (chip) chip.remove(); return; }
    if (!chip) {
      chip = document.createElement("div");
      chip.id = "ec-chip";
      document.body.appendChild(chip);
      chip.addEventListener("click", function () {
        ls(K_NUID, "");
        modal(null);
      });
    }
    chip.innerHTML = '<span>&#10003; checked in</span> &middot;&#8226;&#8226;&#8226;&#8226;' +
                     n.slice(-4) + ' <em>change</em>';
  }

  function toast(msg) {
    var t = document.createElement("div");
    t.className = "ec-toast";
    t.textContent = msg;
    document.body.appendChild(t);
    setTimeout(function () { t.remove(); }, 2600);
  }

  /* ---------- the gate every vote passes through ---------- */

  function ready(pollId, go) {
    var proceed = function () {
      isOpen(pollId).then(function (open) {
        if (!open) { toast("Voting isn't open for this question yet."); return; }
        go();
      });
    };
    if (nuid()) { proceed(); return; }
    modal(function () { proceed(); });   // skipping still votes, just uncredited
  }

  /* ---------- instructor controls ---------- */

  function mountInstructorBar() {
    if (!INSTRUCTOR) return;
    var bar = document.createElement("div");
    bar.id = "ec-instr";
    bar.innerHTML = '<button data-a="open">Open voting</button>' +
                    '<button data-a="close">Close voting</button>' +
                    '<span id="ec-instr-pid"></span>';
    document.body.appendChild(bar);

    function currentPoll() {
      var sec = document.querySelector("section.present");
      var g = sec && sec.querySelector("[data-poll-id]");
      return g ? g.getAttribute("data-poll-id") : null;
    }
    function refresh() {
      var pid = currentPoll();
      bar.style.display = pid ? "flex" : "none";
      bar.querySelector("#ec-instr-pid").textContent = pid || "";
    }
    bar.addEventListener("click", function (e) {
      var a = e.target.getAttribute && e.target.getAttribute("data-a");
      if (!a) return;
      var pid = currentPoll();
      if (pid) (a === "open" ? openPoll : closePoll)(pid);
    });
    if (window.Reveal && Reveal.addEventListener) {
      Reveal.addEventListener("slidechanged", refresh);
    }
    setInterval(refresh, 1000);
    refresh();
  }

  /* ---------- styles ---------- */

  var css = document.createElement("style");
  css.textContent =
    "#ec-checkin{position:fixed;inset:0;z-index:99999;background:rgba(15,23,42,.72);" +
      "display:flex;align-items:center;justify-content:center;font-family:system-ui,-apple-system,sans-serif}" +
    ".ec-ci-card{background:#fff;border-radius:16px;padding:26px 30px;max-width:430px;width:90%;" +
      "box-shadow:0 20px 60px rgba(0,0,0,.35);text-align:center;color:#1f2937}" +
    ".ec-ci-card h3{margin:0 0 8px;font-size:22px;color:#1e3a8a}" +
    ".ec-ci-card p{margin:0 0 14px;font-size:14px;line-height:1.5;color:#4b5563}" +
    "#ec-ci-input{width:100%;box-sizing:border-box;font-size:26px;letter-spacing:5px;text-align:center;" +
      "padding:10px;border:2px solid #cbd5e1;border-radius:10px;font-family:ui-monospace,monospace}" +
    "#ec-ci-input:focus{outline:none;border-color:#2563eb}" +
    "#ec-ci-err{color:#dc2626;font-size:13px;min-height:18px;margin:6px 0}" +
    ".ec-ci-row{display:flex;gap:10px}" +
    ".ec-ci-row button{flex:1;padding:12px;font-size:16px;font-weight:700;border:0;" +
      "border-radius:10px;cursor:pointer}" +
    "#ec-ci-go{color:#fff;background:#2563eb;flex:2}" +
    "#ec-ci-cancel{color:#475569;background:#e2e8f0}" +
    "#ec-ci-cancel:hover{background:#cbd5e1}" +
    "#ec-ci-go:hover{background:#1d4ed8}" +
    ".ec-ci-skip{font-size:11.5px!important;color:#9ca3af!important;margin:12px 0 0!important}" +
    "#ec-chip{position:fixed;right:10px;bottom:10px;z-index:9998;background:rgba(30,58,138,.92);color:#fff;" +
      "font:600 11px/1 system-ui,sans-serif;padding:7px 10px;border-radius:999px;cursor:pointer;opacity:.75}" +
    "#ec-chip:hover{opacity:1}" +
    "#ec-chip em{font-style:normal;text-decoration:underline;opacity:.8}" +
    ".ec-toast{position:fixed;left:50%;bottom:64px;transform:translateX(-50%);z-index:99999;" +
      "background:rgba(17,24,39,.94);color:#fff;font:600 14px/1.3 system-ui,sans-serif;" +
      "padding:11px 18px;border-radius:10px}" +
    "#ec-instr{position:fixed;left:10px;bottom:10px;z-index:9998;display:none;gap:6px;align-items:center;" +
      "background:rgba(17,24,39,.9);padding:6px 8px;border-radius:10px}" +
    "#ec-instr button{font:600 11px system-ui,sans-serif;padding:5px 9px;border:0;border-radius:6px;cursor:pointer}" +
    "#ec-instr span{color:#9ca3af;font:500 10px ui-monospace,monospace}";
  document.head.appendChild(css);

  /* ---------- boot ---------- */

  window.Poll = {
    deviceId:   deviceId,
    nuid:       nuid,
    sessionKey: sessionKey,
    q:          q,
    stamp:      stamp,
    ready:      ready,
    isOpen:     isOpen,
    openPoll:   openPoll,
    closePoll:  closePoll,
    checkIn:    function () { modal(null); },
    toast:      toast
  };

  function boot() {
    probeSessionKey();
    paintChip();
    mountInstructorBar();
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else { boot(); }
})();
