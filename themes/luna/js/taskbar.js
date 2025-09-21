// Taskbar Controller  [SKETCH]
// Responsible for taskbar logic ( Start menu, Taskbar bubbles, Widgets, etc. )
// Robin Universe [S]
// 09 . 11 . 25

Taskbar = document.getElementById("Tasks");

// Bubble template
const bubble = ({ PID, title, icon }) => `
<div id="${PID}_bubble" class="bubble" title="${PID}" onclick="toggleActiveBubble(${PID}, true)">
    <div id="bubbleWrapper" >
        <img class="shadow" src="${icon}" width="16" height="16"> ${title}
    </div>
    </br>
</div>
`;

// Make one bubble active and deactivate all other bubbles
function toggleActiveBubble(PID, ftb=false){
    document.querySelectorAll('.activebubble').forEach(el => el.classList.remove('activebubble'));
    element = document.getElementById(PID + '_bubble');
    element.classList.toggle('activebubble');
    if (ftb) { // "From Task Bar" flag tells this function to also set the attributed window to active as well
        document.querySelectorAll('.active').forEach(el => el.classList.remove('active'));
        element = document.getElementById(PID + '_window');
        element.classList.remove('minimized'); 
        element.classList.toggle('active');
    } 
}

// Insert a new bubble into the taskbar
function spawnBubble(PID){
    
    // Get the element from the PID so we can grab the title and icon
    element = document.getElementById(PID + '_window');
    title   = element.title
    icon    = element.children[0].children[0].firstElementChild.src
    
    //insert bubble div 
    Taskbar.insertAdjacentHTML('beforeend', bubble({ PID, title, icon }));
    
    // mark as active when created
    toggleActiveBubble(PID)
}

// Destroy a bubble when it's program is closed
function destroyBubble(PID){
    var element = document.getElementById(PID + '_bubble');
    element.remove();
}

// Simple 12HR clock
function startTime() {
    const today = new Date();
    let h = today.getHours();
    let m = today.getMinutes();
    let ampm = "";

    if (h >= 12) { ampm = "PM"; if (h > 12) { h = h - 12; } } else { ampm = "AM"; if (h === 0) { h = 12; } }

    m = checkTime(m);

    document.getElementById("clock").innerHTML = h + ":" + m + ampm;
    setTimeout(startTime, 1000);
}

// Make it double-digit
function checkTime(i) {
    if (i < 10) { i = "0" + i; }
    return i;
}

startTime();

window.addEventListener("window:created",  e => spawnBubble(e.detail.PID));
window.addEventListener("window:focused",  e => toggleActiveBubble(e.detail.PID));
window.addEventListener("window:closed",   e => destroyBubble(e.detail.PID));
