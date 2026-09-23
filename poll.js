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

  var IS_FILE = (window.location.protocol === "file:");
  var qs      = new URLSearchParams(window.location.search);

  // Which window are we? Mirrors presenter-gate v5's detection exactly.
  //   PROJECTOR — the deck the room sees (?presenter). Owns auto open/close.
  //   SPEAKER   — the current-slide preview INSIDE reveal's speaker view.
  //               Renders the status bar and the manual overrides.
  //   A student's deck is neither, so it never loads the secret and never
  //   touches a window.
  var Q          = location.search;
  var PROJECTOR  = /[?&]presenter(&|=|$)/.test(Q);
  var SPEAKER    = /[?&]receiver(&|$)/.test(Q) && /postMessageEvents=true/.test(Q);
  var INSTRUCTOR = PROJECTOR || SPEAKER || qs.has("instructor");

  var GRACE_MS = 20000;   // keep a poll open this long after leaving its slide

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

  function openPoll(pollId)  { return windowRpc("open_poll",  pollId); }
  function closePoll(pollId) { return windowRpc("close_poll", pollId); }

  /* ---------- instructor secret, via the shared CCGate passphrase ---------- */
  // The Supabase secret is a random machine string nobody types. It lives
  // encrypted in poll-secret.js under the SAME passphrase that unlocks
  // /poll-admin/ and /class-console/, and CCGate caches that passphrase
  // origin-wide as "cc.pass". So unlocking any instructor page in this
  // browser makes this silent forever after.
  //
  // Silent-only on the PROJECTOR: mounting CCGate's full-screen gate there
  // would cover the slide in front of the room. The gate is only ever shown
  // in speaker view.

  var secretPromise = null;

  function b64(str) { return Uint8Array.from(atob(str), function (c) { return c.charCodeAt(0); }); }

  function ccDecrypt(payload, pass) {
    var enc = new TextEncoder();
    return crypto.subtle
      .importKey("raw", enc.encode(pass), "PBKDF2", false, ["deriveKey"])
      .then(function (base) {
        return crypto.subtle.deriveKey(
          { name: "PBKDF2", salt: b64(payload.salt), iterations: payload.iter, hash: "SHA-256" },
          base, { name: "AES-GCM", length: 256 }, false, ["decrypt"]);
      })
      .then(function (key) {
        return crypto.subtle.decrypt({ name: "AES-GCM", iv: b64(payload.iv) }, key, b64(payload.ct));
      })
      .then(function (clear) { return JSON.parse(new TextDecoder().decode(clear)); });
  }

  function loadScript(src) {
    return new Promise(function (resolve, reject) {
      var el = document.createElement("script");
      el.src = src; el.onload = resolve; el.onerror = reject;
      document.head.appendChild(el);
    });
  }

  function base() {   // poll.js sits at the repo root, two levels above a deck
    var tag = document.querySelector('script[src$="poll.js"]');
    return tag ? tag.getAttribute("src").replace(/poll\.js$/, "") : "../../";
  }

  // Fetched, never <script src>. A script tag is cached by the browser, so
  // after a passphrase rotation the page keeps the OLD payload and the correct
  // passphrase can never open it -- silently, because the projector suppresses
  // every message. no-store is the whole point of this function.
  function loadPayload() {
    return fetch(base() + "poll-secret.js", { cache: "no-store" })
      .then(function (r) { return r.ok ? r.text() : null; })
      .then(function (t) {
        if (!t) return null;
        var m = t.match(/=\s*(\{[\s\S]*?\})\s*;/);
        return m ? JSON.parse(m[1]) : null;
      })
      .catch(function () { return null; });
  }

  function instructorSecret() {
    if (secretPromise) return secretPromise;
    secretPromise = new Promise(function (resolve) {
      if (!INSTRUCTOR || IS_FILE || !(window.crypto && crypto.subtle)) return resolve(null);
      loadPayload()
        .then(function (pl) {
          if (!pl) return resolve(null);
          var cached = ls("cc.pass");
          if (cached) {
            return ccDecrypt(pl, cached.trim())
              .then(function (d) { resolve(d && d.poll_secret || null); })
              .catch(function () { gate(pl, resolve); });      // stale passphrase
          }
          gate(pl, resolve);
        })
        .catch(function () { resolve(null); });     // no poll-secret.js yet
    });
    return secretPromise;
  }

  // Only reachable from speaker view / ?instructor, never from the projector.
  function gate(payload, resolve) {
    if (!SPEAKER && !qs.has("instructor")) return resolve(null);
    loadScript(base() + "auth.js")
      .then(function () {
        if (!window.CCGate) return resolve(null);
        window.CCGate.mount({
          payload: payload,
          title: "Instructor passphrase (same one as poll-admin)",
          onUnlock: function (d) { resolve(d && d.poll_secret || null); }
        });
      })
      .catch(function () { resolve(null); });
  }

  function windowRpc(fn, pollId) {
    return instructorSecret().then(function (secret) {
      // Anything that goes wrong here must stay off the projected screen.
      // Only speaker view is allowed to say a word about it, and the fallback
      // is always "windows unused" -> voting open, never a dead room.
      var say = SPEAKER ? toast : function () {};
      if (!secret) { say("No instructor secret on this device."); return false; }
      return rpc(fn, { p_poll_id: pollId, p_session_key: sessionKey(), p_pass: secret })
        .then(function (r) {
          if (!r.ok) { secretPromise = null; say("Server rejected the instructor secret."); return false; }
          windowCache[pollId] = null;
          paintSpeakerBar();
          return true;
        })
        .catch(function () { say("Could not reach the server."); return false; });
    });
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

  /* ---------- auto open/close, driven by the slide ---------- */
  // The point of this block: you never have to remember anything. Walking
  // onto a poll slide opens voting; walking off it closes voting after a
  // grace period, so a student mid-tap is not cut off. Speaker view shows
  // the state and can override it.

  var openIds = {};        // pollId -> true while we believe it is open
  var closeTimers = {};    // pollId -> timeout id
  var pinned = {};         // pollId -> true: "keep open", survives leaving

  function pollIdsOnCurrentSlide() {
    var sec = document.querySelector("section.present");
    if (!sec) return [];
    var out = [];
    [].forEach.call(sec.querySelectorAll("[data-poll-id]"), function (e) {
      var id = e.getAttribute("data-poll-id");
      if (id && out.indexOf(id) < 0) out.push(id);
    });
    return out;
  }

  function onSlideChanged() {
    var here = pollIdsOnCurrentSlide();

    here.forEach(function (id) {
      if (closeTimers[id]) { clearTimeout(closeTimers[id]); delete closeTimers[id]; }
      if (openIds[id]) return;
      openIds[id] = "pending";
      openPoll(id).then(function (ok) {
        if (ok) openIds[id] = true;
        else delete openIds[id];      // failed: leave windows unused, retry on re-entry
        paintSpeakerBar();
      });
    });

    Object.keys(openIds).forEach(function (id) {
      if (here.indexOf(id) >= 0 || pinned[id] || closeTimers[id]) return;
      if (openIds[id] !== true) { delete openIds[id]; return; }
      closeTimers[id] = setTimeout(function () {
        delete closeTimers[id];
        delete openIds[id];
        closePoll(id);
      }, GRACE_MS);
    });

    paintSpeakerBar();
  }

  /* ---------- speaker-view status bar ---------- */
  // Rendered ONLY inside reveal's speaker-view preview. The projected deck
  // never shows it, so the room never sees the controls.

  function mountSpeakerBar() {
    if (!SPEAKER) return;
    var bar = document.createElement("div");
    bar.id = "ec-spk";
    bar.innerHTML =
      '<span id="ec-spk-dot"></span>' +
      '<span id="ec-spk-state">—</span>' +
      '<span id="ec-spk-count"></span>' +
      '<span id="ec-spk-grow"></span>' +
      '<button data-a="pin"   type="button">Keep open</button>' +
      '<button data-a="close" type="button">Close now</button>';
    document.body.appendChild(bar);

    bar.addEventListener("click", function (e) {
      var a = e.target.getAttribute && e.target.getAttribute("data-a");
      if (!a) return;
      var ids = pollIdsOnCurrentSlide();
      if (!ids.length) return;
      ids.forEach(function (id) {
        if (a === "pin") {
          pinned[id] = !pinned[id];
          if (pinned[id]) {
            if (closeTimers[id]) { clearTimeout(closeTimers[id]); delete closeTimers[id]; }
            if (!openIds[id]) { openIds[id] = true; openPoll(id); }
          }
        } else {
          if (closeTimers[id]) { clearTimeout(closeTimers[id]); delete closeTimers[id]; }
          pinned[id] = false;
          delete openIds[id];
          closePoll(id);
        }
      });
      paintSpeakerBar();
    });

    setInterval(paintSpeakerBar, 3000);
    paintSpeakerBar();
  }

  function paintSpeakerBar() {
    var bar = document.getElementById("ec-spk");
    if (!bar) return;
    var ids = pollIdsOnCurrentSlide();
    if (!ids.length) { bar.style.display = "none"; return; }
    bar.style.display = "flex";

    var id = ids[0];
    var dot = bar.querySelector("#ec-spk-dot");
    var st  = bar.querySelector("#ec-spk-state");
    var ct  = bar.querySelector("#ec-spk-count");
    var pin = bar.querySelector('[data-a="pin"]');

    isOpen(id).then(function (open) {
      var closing = !!closeTimers[id];
      dot.className = open ? (closing ? "amber" : "green") : "red";
      st.textContent = open ? (closing ? "CLOSING…" : "VOTING OPEN") : "CLOSED";
      pin.textContent = pinned[id] ? "Unpin" : "Keep open";
      pin.className   = pinned[id] ? "on" : "";
    });

    if (!IS_FILE) {
      sf("GET", "poll_votes?poll_id=eq." + encodeURIComponent(id) + "&select=choice" + q())
        .then(function (r) { return r.ok ? r.json() : []; })
        .then(function (rows) {
          ct.textContent = rows.length + (rows.length === 1 ? " vote" : " votes");
        })
        .catch(function () {});
    }
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
    "#ec-spk{position:fixed;top:0;left:0;right:0;z-index:9998;display:none;gap:10px;" +
      "align-items:center;padding:7px 12px;background:#111827;color:#fff;" +
      "font:600 13px/1 system-ui,-apple-system,sans-serif}" +
    "#ec-spk-dot{width:11px;height:11px;border-radius:50%;background:#6b7280;flex:none}" +
    "#ec-spk-dot.green{background:#22c55e;box-shadow:0 0 0 3px rgba(34,197,94,.25)}" +
    "#ec-spk-dot.amber{background:#f59e0b;box-shadow:0 0 0 3px rgba(245,158,11,.25)}" +
    "#ec-spk-dot.red{background:#ef4444}" +
    "#ec-spk-count{color:#9ca3af;font-weight:500}" +
    "#ec-spk-grow{flex:1}" +
    "#ec-spk button{font:600 11px system-ui,sans-serif;padding:5px 10px;border:0;" +
      "border-radius:6px;cursor:pointer;background:#374151;color:#e5e7eb}" +
    "#ec-spk button:hover{background:#4b5563}" +
    "#ec-spk button.on{background:#f59e0b;color:#111827}";
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
    pollIdsHere: pollIdsOnCurrentSlide,
    toast:      toast
  };

  function boot() {
    probeSessionKey();
    paintChip();
    mountSpeakerBar();
    if (PROJECTOR || SPEAKER) {
      if (window.Reveal && Reveal.addEventListener) {
        Reveal.addEventListener("slidechanged", function () {
          // only the projector drives the windows; speaker view just redraws
          if (PROJECTOR) onSlideChanged(); else paintSpeakerBar();
        });
      }
      if (PROJECTOR) onSlideChanged();
    }
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else { boot(); }
})();
