// Desktop window management logic
// Responsible for window movement, minimizing, layering, etc
// oh god this one got big sorry
// Robin Universe [D]
// 09 . 11 . 25

(() => {
  // what the fucking kind of windows. is this.
  var scriptUrl = document.currentScript.src; 
  var url = new URL(scriptUrl);
  var params = new URLSearchParams(url.search);
  var PID = params.get('PID');

  var winEl   = document.getElementById(PID + '_window');
  var handle  = document.getElementById(PID + '_handle');
  var iframe  = document.getElementById(PID + '_iframe');
  var bubble  = document.getElementById(PID + '_bubble');

  var dragging = false;
  var startX = 0, startY = 0;
  var startLeft = 0, startTop = 0;

  // WM Button stuff
  var btnClose = document.getElementById(PID + '_close');
  var btnMin   = document.getElementById(PID + '_min');
  var btnMax   = document.getElementById(PID + '_max');

  // Close the window by destroying it, it's children and then this script
  btnClose?.addEventListener('pointerdown', () => {
    // make a window destruction event for the taskbar to listen to eventually...
    window.dispatchEvent(new CustomEvent("window:closed", { detail: { PID } }));

    iframe.remove();
    handle.remove();
    winEl.remove();
  });

  // just toggle a class for the minimization, CSS can do the rest
  btnMin?.addEventListener('pointerdown', () => {
    winEl.classList.toggle('minimized');
    winEl.classList.remove('active'); 
    bubble.classList.remove('activebubble'); 
  });

  // call a maximize function so we can maximize from multiple methods (hotkeys maybe someday?)
  btnMax?.addEventListener('pointerdown', () => {
    maximizeWindow();
  });

  function maximizeWindow(){
    winEl.classList.toggle('maximized');

    if (winEl.classList.contains('maximized')){
      console.log(PID + " maximized") // This could probably be a CSS rule...
      winEl.style.left    = 0;
      winEl.style.top     = -27;
      winEl.style.width   = "100.75%";
      winEl.style.height  = "103.75%";
    } else {
      console.log(PID + " un-maximized"); // @TODO: Memorize window size/pos so it can be restored
      winEl.style.left    = "10%";
      winEl.style.top     = "10%";
      winEl.style.width   = "60%";
      winEl.style.height  = "80%";
    }
  }

  // focus the window ( just toggles a class that is at a slightly higher z-index )
  function focusWindow() {
    
    document.querySelectorAll('.active').forEach(el => el.classList.remove('active'));
    winEl.classList.add('active');

    window.dispatchEvent(new CustomEvent("window:focused", { detail: { PID } }));
  }

  winEl.addEventListener('pointerdown', focusWindow);
  iframe?.addEventListener('pointerdown', focusWindow, { capture: true });

  // window drag stuff
  handle.addEventListener('pointerdown', (e) => {
    // Do not let maximized windows move
    if (winEl.classList.contains("maximized")) return;

    // takes a drag
    dragging = true;
    document.body.classList.add('no-select');
    iframe.style.pointerEvents = 'none';           // prevent iframe from eating events
    handle.setPointerCapture(e.pointerId);         // keep events even if pointer leaves handle (this sucks)

    // record starting positions
    startX = e.clientX;
    startY = e.clientY;

    startLeft = parseInt(getComputedStyle(winEl).left, 10) || 0;
    startTop  = parseInt(getComputedStyle(winEl).top, 10)  || 0;
  });

  // maximize when the titlebar is doubleclicked
  handle.addEventListener('dblclick', (e) => {
    maximizeWindow();
  });

  // main mouse movement shit
  handle.addEventListener('pointermove', (e) => {
    if (!dragging) return;

    const dx = e.clientX - startX;
    const dy = e.clientY - startY;

    // new position
    let nextLeft = startLeft + dx;
    let nextTop  = startTop  + dy;

    winEl.style.left = `${nextLeft}px`;
    winEl.style.top  = `${nextTop}px`;
  });

  // need to do this to make sure we don't drop inputs
  var endDrag = (e) => {
    if (!dragging) return;
    dragging = false;
    document.body.classList.remove('no-select');
    iframe.style.pointerEvents = '';
    if (e && e.pointerId != null) {
      try { handle.releasePointerCapture(e.pointerId); } catch {}
    }
  };

  // make the mouse not feel weird
  handle.addEventListener('pointerup', endDrag);
  handle.addEventListener('pointercancel', endDrag);
  handle.addEventListener('lostpointercapture', endDrag);

  // make sure the window is focused when it's first spawned
  window.dispatchEvent(new CustomEvent("window:created", { detail: { PID } }));
  focusWindow();
})();