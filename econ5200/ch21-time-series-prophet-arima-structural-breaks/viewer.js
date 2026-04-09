/**
 * Lecture Viewer — RevealJS Wrapper
 * Features: presenter/student/overview modes, dual-monitor sync,
 * timer with pace indicator, laser pointer, black screen, jump-to-slide.
 * Handles file:// with graceful degradation + connection banner.
 */

(function () {
  'use strict';

  // ── Configuration (injected by build-viewer) ──
  const CONFIG = {
    presentationPath: '../presentation.html',
    classDuration: 75,
    lectureTitle: 'Time Series II: Prophet, ARIMA & Structural Breaks'
  };

  // ── DOM References ──
  const frame = document.getElementById('slide-frame');
  const currentSlideEl = document.getElementById('current-slide');
  const totalSlidesEl = document.getElementById('total-slides');
  const notesEl = document.getElementById('speaker-notes-content');
  const nextSlideEl = document.getElementById('next-slide-content');
  const timerBar = document.getElementById('timer-bar');
  const timerElapsed = document.getElementById('timer-elapsed');
  const timerRemaining = document.getElementById('timer-remaining');
  const timerProgressFill = document.getElementById('timer-progress-fill');
  const paceIndicator = document.getElementById('pace-indicator');
  const overviewGrid = document.getElementById('overview-grid');
  const shortcutsOverlay = document.getElementById('shortcuts-overlay');
  const connectionBanner = document.getElementById('connection-banner');
  const blackScreen = document.getElementById('black-screen');
  const laserPointer = document.getElementById('laser-pointer');
  const slideArea = document.getElementById('slide-area');

  // ── State ──
  let revealReady = false;
  let currentSlide = 0;
  let totalSlides = 0;
  let timerRunning = false;
  let timerStartTime = null;
  let timerPausedElapsed = 0;
  let timerInterval = null;
  let laserActive = false;
  let blackScreenActive = false;
  let studentWindow = null;
  let notesFontSize = 14;
  let jumpBuffer = '';
  let jumpTimeout = null;

  // ── Session Persistence ──
  function saveTimerState() {
    try {
      sessionStorage.setItem('viewer-timer', JSON.stringify({
        running: timerRunning,
        startTime: timerStartTime,
        pausedElapsed: timerPausedElapsed
      }));
    } catch (e) {}
  }

  function restoreTimerState() {
    try {
      var saved = JSON.parse(sessionStorage.getItem('viewer-timer'));
      if (saved && saved.startTime) {
        // Sanity check: discard if elapsed exceeds 2× class duration (stale session)
        var elapsed = (saved.pausedElapsed || 0);
        if (saved.running) {
          elapsed += (Date.now() - saved.startTime) / 1000;
        }
        if (elapsed > CONFIG.classDuration * 60 * 2 || elapsed < 0) {
          sessionStorage.removeItem('viewer-timer');
          return;
        }

        timerPausedElapsed = saved.pausedElapsed || 0;
        if (saved.running) {
          timerStartTime = saved.startTime;
          timerRunning = true;
          timerInterval = setInterval(updateTimer, 1000);
          document.getElementById('timer-start').hidden = true;
          document.getElementById('timer-pause').hidden = false;
          updateTimer();
        }
      }
    } catch (e) {}
  }

  // ── Reveal.js Communication ──

  frame.addEventListener('load', function () {
    // Exponential backoff: 200, 400, 800, 1600, 3200ms
    let delay = 200;
    let attempts = 0;
    const maxAttempts = 8; // ~15 seconds total

    function tryConnect() {
      attempts++;
      try {
        const win = frame.contentWindow;
        if (win && win.Reveal && win.Reveal.isReady && win.Reveal.isReady()) {
          revealReady = true;
          connectionBanner.hidden = true;
          onRevealReady(win.Reveal);
          return;
        }
      } catch (e) {
        // Cross-origin (file://) — show connection banner
        connectionBanner.hidden = false;
        console.warn('Viewer: Cross-origin iframe. Use a local server for full features.');
        return;
      }

      if (attempts < maxAttempts) {
        delay = Math.min(delay * 2, 3200);
        setTimeout(tryConnect, delay);
      } else {
        connectionBanner.hidden = false;
      }
    }

    setTimeout(tryConnect, 200);
  });

  function onRevealReady(Reveal) {
    totalSlides = Reveal.getTotalSlides();
    totalSlidesEl.textContent = totalSlides;
    updateSlideInfo(Reveal);

    Reveal.on('slidechanged', function () {
      updateSlideInfo(Reveal);
      syncStudentWindow();
    });
  }

  function updateSlideInfo(Reveal) {
    var slides = Reveal.getSlides();
    var cur = Reveal.getCurrentSlide();
    var slideNum = 0;
    for (var i = 0; i < slides.length; i++) {
      slideNum++;
      if (slides[i] === cur) break;
    }
    currentSlide = slideNum;
    currentSlideEl.textContent = slideNum;

    // Speaker notes
    var notes = Reveal.getSlideNotes();
    notesEl.innerHTML = notes || '<em>No speaker notes for this slide.</em>';

    // Next slide preview — show heading + first content line
    if (slideNum < slides.length) {
      var next = slides[slideNum];
      if (next) {
        var heading = next.querySelector('h1, h2, h3');
        var content = next.querySelector('p, li');
        var preview = heading ? heading.textContent : '(next slide)';
        if (content && content.textContent.length > 0) {
          preview += '\n' + content.textContent.substring(0, 100);
        }
        nextSlideEl.textContent = preview;
      }
    } else {
      nextSlideEl.textContent = '(last slide)';
    }

    // Update pace indicator
    updatePaceIndicator();
  }

  // ── Navigation ──

  function nextSlideAction() {
    if (!revealReady) return;
    try { frame.contentWindow.Reveal.next(); } catch (e) {}
  }

  function prevSlideAction() {
    if (!revealReady) return;
    try { frame.contentWindow.Reveal.prev(); } catch (e) {}
  }

  function goToSlide(index) {
    if (!revealReady) return;
    try {
      var slides = frame.contentWindow.Reveal.getSlides();
      if (slides[index]) {
        var h = parseInt(slides[index].getAttribute('data-index-h')) || 0;
        var v = parseInt(slides[index].getAttribute('data-index-v')) || 0;
        frame.contentWindow.Reveal.slide(h, v);
      }
    } catch (e) {}
  }

  // Jump to slide: press G to enter jump mode, then type digits
  function startJumpMode() {
    jumpBuffer = 'G';  // sentinel: jump mode active
    clearTimeout(jumpTimeout);
    // Auto-cancel jump mode if no digits within 2 seconds
    jumpTimeout = setTimeout(function () { jumpBuffer = ''; }, 2000);
  }

  function handleJumpKey(digit) {
    if (jumpBuffer === 'G') jumpBuffer = '';  // clear sentinel, start collecting digits
    jumpBuffer += digit;
    clearTimeout(jumpTimeout);
    jumpTimeout = setTimeout(function () {
      var num = parseInt(jumpBuffer);
      if (num >= 1 && num <= totalSlides) {
        goToSlide(num - 1);
      }
      jumpBuffer = '';
    }, 800);
  }

  // ── Multi-Window Sync (dual monitor) ──

  // ── Multi-Window Sync ──
  var syncChannel = null;

  function openStudentWindow() {
    if (studentWindow && !studentWindow.closed) {
      studentWindow.focus();
      return;
    }
    studentWindow = window.open(CONFIG.presentationPath, 'student-view',
      'width=1280,height=720,menubar=no,toolbar=no,location=no');

    // Set up BroadcastChannel for cross-origin sync fallback
    if (window.BroadcastChannel && !syncChannel) {
      syncChannel = new BroadcastChannel('lecture-viewer-sync');
      syncChannel.onmessage = function (e) {
        // Listen for sync messages from other tabs (if student window sends back)
        if (e.data && e.data.type === 'slide-sync' && e.data.source === 'student') {
          // Student window acknowledged — no action needed
        }
      };
    }
  }

  function syncStudentWindow() {
    if (!studentWindow || studentWindow.closed) return;

    // Try direct Reveal API first (same-origin)
    try {
      if (studentWindow.Reveal && studentWindow.Reveal.isReady()) {
        var indices = frame.contentWindow.Reveal.getIndices();
        studentWindow.Reveal.slide(indices.h, indices.v, indices.f);
        return;
      }
    } catch (e) {}

    // Fallback: BroadcastChannel (works cross-origin if student window listens)
    if (syncChannel) {
      try {
        var indices = frame.contentWindow.Reveal.getIndices();
        syncChannel.postMessage({ type: 'slide-sync', source: 'presenter', h: indices.h, v: indices.v, f: indices.f });
      } catch (e) {}
    }
  }

  // ── Mode Switching ──

  function setMode(mode) {
    document.body.setAttribute('data-mode', mode);

    document.getElementById('btn-presenter').classList.toggle('active', mode === 'presenter');
    document.getElementById('btn-student').classList.toggle('active', mode === 'student');
    document.getElementById('btn-overview').classList.toggle('active', mode === 'overview');

    document.querySelector('.presenter-layout').hidden = (mode === 'overview');
    document.querySelector('.overview-layout').hidden = (mode !== 'overview');

    // Timer visible by default in presenter mode
    if (mode === 'presenter') {
      timerBar.hidden = false;
    } else if (mode === 'student') {
      timerBar.hidden = true;
    }

    if (mode === 'overview') buildOverview();
  }

  function buildOverview() {
    if (!revealReady) return;
    overviewGrid.innerHTML = '';
    try {
      var slides = frame.contentWindow.Reveal.getSlides();
      slides.forEach(function (slide, i) {
        var thumb = document.createElement('div');
        thumb.className = 'overview-thumb';
        if (i === currentSlide - 1) thumb.classList.add('current');

        var heading = slide.querySelector('h1, h2, h3');
        var title = heading ? heading.textContent : 'Slide ' + (i + 1);

        thumb.innerHTML =
          '<div class="thumb-number">' + (i + 1) + '</div>' +
          '<div class="thumb-title">' + title + '</div>';

        thumb.addEventListener('click', function () {
          goToSlide(i);
          setMode('presenter');
        });

        overviewGrid.appendChild(thumb);
      });
    } catch (e) {}
  }

  // ── Timer ──

  function formatTime(seconds) {
    var m = Math.floor(seconds / 60);
    var s = Math.floor(seconds % 60);
    return (m < 10 ? '0' : '') + m + ':' + (s < 10 ? '0' : '') + s;
  }

  function updateTimer() {
    if (!timerRunning) return;
    var now = Date.now();
    var elapsed = timerPausedElapsed + (now - timerStartTime) / 1000;
    var totalSeconds = CONFIG.classDuration * 60;
    var remaining = Math.max(0, totalSeconds - elapsed);
    var progress = Math.min(100, (elapsed / totalSeconds) * 100);

    timerElapsed.textContent = formatTime(elapsed);
    timerRemaining.textContent = formatTime(remaining);
    timerProgressFill.style.width = progress + '%';

    // Color coding with pulse at thresholds
    if (progress > 90) {
      timerProgressFill.style.backgroundColor = 'var(--timer-danger)';
      if (!timerProgressFill.classList.contains('pulsed-90')) {
        timerProgressFill.classList.add('pulse', 'pulsed-90');
        setTimeout(function () { timerProgressFill.classList.remove('pulse'); }, 2000);
      }
    } else if (progress > 75) {
      timerProgressFill.style.backgroundColor = 'var(--timer-warn)';
      if (!timerProgressFill.classList.contains('pulsed-75')) {
        timerProgressFill.classList.add('pulse', 'pulsed-75');
        setTimeout(function () { timerProgressFill.classList.remove('pulse'); }, 2000);
      }
    } else {
      timerProgressFill.style.backgroundColor = 'var(--accent)';
    }

    saveTimerState();
  }

  function updatePaceIndicator() {
    if (!timerRunning || totalSlides === 0) {
      paceIndicator.textContent = '';
      return;
    }
    var elapsed = timerPausedElapsed + (Date.now() - timerStartTime) / 1000;
    var totalSeconds = CONFIG.classDuration * 60;
    var timeProgress = elapsed / totalSeconds;
    var slideProgress = currentSlide / totalSlides;

    if (slideProgress > timeProgress + 0.1) {
      paceIndicator.textContent = 'Ahead';
      paceIndicator.className = 'pace-indicator pace-ahead';
    } else if (slideProgress < timeProgress - 0.1) {
      paceIndicator.textContent = 'Behind';
      paceIndicator.className = 'pace-indicator pace-behind';
    } else {
      paceIndicator.textContent = 'On pace';
      paceIndicator.className = 'pace-indicator pace-ok';
    }
  }

  function startTimer() {
    timerRunning = true;
    timerStartTime = Date.now();
    timerInterval = setInterval(updateTimer, 1000);
    document.getElementById('timer-start').hidden = true;
    document.getElementById('timer-pause').hidden = false;
    updateTimer();
  }

  function pauseTimer() {
    if (!timerRunning) return;
    timerRunning = false;
    timerPausedElapsed += (Date.now() - timerStartTime) / 1000;
    clearInterval(timerInterval);
    document.getElementById('timer-start').hidden = false;
    document.getElementById('timer-pause').hidden = true;
    saveTimerState();
  }

  function resetTimer() {
    timerRunning = false;
    timerPausedElapsed = 0;
    timerStartTime = null;
    clearInterval(timerInterval);
    timerElapsed.textContent = '00:00';
    timerRemaining.textContent = formatTime(CONFIG.classDuration * 60);
    timerProgressFill.style.width = '0%';
    timerProgressFill.style.backgroundColor = 'var(--accent)';
    timerProgressFill.classList.remove('pulse', 'pulsed-75', 'pulsed-90');
    document.getElementById('timer-start').hidden = false;
    document.getElementById('timer-pause').hidden = true;
    paceIndicator.textContent = '';
    saveTimerState();
  }

  // ── Laser Pointer ──

  function toggleLaser() {
    laserActive = !laserActive;
    document.getElementById('btn-laser').classList.toggle('active', laserActive);
    laserPointer.hidden = !laserActive;
    slideArea.style.cursor = laserActive ? 'none' : '';
  }

  slideArea.addEventListener('mousemove', function (e) {
    if (!laserActive) return;
    var rect = slideArea.getBoundingClientRect();
    laserPointer.style.left = (e.clientX - rect.left - 6) + 'px';
    laserPointer.style.top = (e.clientY - rect.top - 6) + 'px';
  });

  // ── Black Screen ──

  function toggleBlackScreen() {
    blackScreenActive = !blackScreenActive;
    blackScreen.hidden = !blackScreenActive;
    document.getElementById('btn-black').classList.toggle('active', blackScreenActive);
  }

  // ── Theme Toggle ──

  function toggleTheme() {
    var themes = ['light', 'dark', 'high-contrast'];
    var current = document.body.getAttribute('data-theme');
    var next = themes[(themes.indexOf(current) + 1) % themes.length];
    document.body.setAttribute('data-theme', next);
  }

  // ── Fullscreen ──

  function toggleFullscreen() {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(function () {});
    } else {
      document.exitFullscreen();
    }
  }

  // ── Notes Font Size ──

  function adjustNotesFontSize(delta) {
    notesFontSize = Math.max(10, Math.min(24, notesFontSize + delta));
    notesEl.style.fontSize = notesFontSize + 'px';
    nextSlideEl.style.fontSize = Math.max(10, notesFontSize - 2) + 'px';
  }

  // ── Event Listeners ──

  document.getElementById('btn-presenter').addEventListener('click', function () { setMode('presenter'); });
  document.getElementById('btn-student').addEventListener('click', function () { setMode('student'); });
  document.getElementById('btn-overview').addEventListener('click', function () { setMode('overview'); });
  document.getElementById('btn-popout').addEventListener('click', openStudentWindow);
  document.getElementById('btn-timer').addEventListener('click', function () {
    timerBar.hidden = !timerBar.hidden;
  });
  document.getElementById('timer-start').addEventListener('click', startTimer);
  document.getElementById('timer-pause').addEventListener('click', pauseTimer);
  document.getElementById('timer-reset').addEventListener('click', resetTimer);
  document.getElementById('btn-laser').addEventListener('click', toggleLaser);
  document.getElementById('btn-black').addEventListener('click', toggleBlackScreen);
  document.getElementById('btn-theme').addEventListener('click', toggleTheme);
  document.getElementById('btn-fullscreen').addEventListener('click', toggleFullscreen);
  document.getElementById('notes-font-up').addEventListener('click', function () { adjustNotesFontSize(2); });
  document.getElementById('notes-font-down').addEventListener('click', function () { adjustNotesFontSize(-2); });

  // Keyboard shortcuts
  document.addEventListener('keydown', function (e) {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

    // Jump-to-slide: G + digits
    if (jumpBuffer !== '' && e.key >= '0' && e.key <= '9') {
      handleJumpKey(e.key);
      return;
    }

    switch (e.key) {
      case 'ArrowRight':
      case ' ':
        e.preventDefault();
        nextSlideAction();
        break;
      case 'ArrowLeft':
        e.preventDefault();
        prevSlideAction();
        break;
      case 'p': case 'P': setMode('presenter'); break;
      case 'u': case 'U': setMode('student'); break;
      case 'o': case 'O': setMode('overview'); break;
      case 'w': case 'W': openStudentWindow(); break;
      case 't': case 'T': timerBar.hidden = !timerBar.hidden; break;
      case 'l': case 'L': toggleLaser(); break;
      case 'b': case 'B': toggleBlackScreen(); break;
      case 'f': case 'F': toggleFullscreen(); break;
      case 'g': case 'G': startJumpMode(); break;
      case '?': shortcutsOverlay.hidden = !shortcutsOverlay.hidden; break;
      case 'Escape':
        shortcutsOverlay.hidden = true;
        if (blackScreenActive) toggleBlackScreen();
        if (laserActive) toggleLaser();
        break;
      default:
        if (jumpBuffer === '' && e.key >= '0' && e.key <= '9') break; // Ignore stray digits
    }
  });

  // ── Initialize ──
  // Load iframe src from config (not hardcoded in HTML)
  frame.src = CONFIG.presentationPath || frame.getAttribute('data-default-src') || '../presentation.html';

  setMode('presenter');
  resetTimer();
  restoreTimerState();

})();
