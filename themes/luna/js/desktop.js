// Desktop background logic
// Responsible for window creation and destruction, shortcuts, and wallpaper stuff
// Robin Universe [S]
// 09 . 11 . 25

// Basic window HTML template to instantiate
Windows = document.getElementById("Windows")

const tpl = ({ PID, title, url, icon }) => `
    <div id="${PID}_window" class="window" title="${title}" >
        <div id="${PID}_handle" class="handle">

            <div id="title">
                <img id="icon" class="shadow" src="../assets/gfx/${icon}" width="16" height="16"> ${title}
            </div>

            <div id="${PID}_WM" class="WM">
                <img src="../assets/gfx/minimizeButton.png" id="${PID}_min">
                <img src="../assets/gfx/maximizeButton.png" id="${PID}_max"> 
                <img src="../assets/gfx/closeButton.png"" id="${PID}_close">
            </div>

        </div>
        <iframe src="${url}" id="${PID}_iframe" class="iframe"></iframe>
    </div>
`;

// Function to toggle the highlighted class on desktop icons
function highlight(element) {
    document.querySelectorAll('.highlighted').forEach(el => el.classList.remove('highlighted'));
    element.classList.toggle('highlighted'); 
  }

// What to do when an icon is doubleclicked
function openShortcut(element) {
    targetURL   = element.lastElementChild.href         // The desired URL of the spawned windows content
    windowTitle = element.innerText                     // The desired title of the window
    windowType  = element.lastElementChild.classList[0] // The type of window (ie, app, etc.,)

    iconURL     = element.children[0].src               // This sucks @TODO: unsuck it
    iconSegs    = iconURL.split("/");
    icon        = iconSegs.pop();

    spawn(windowType, windowTitle, targetURL, icon)
}

// RNG for window PIDs
function getRandomInt(max) { return Math.floor(Math.random() * max); }

// Function to spawn a new window
function spawn(type, title, target, icon="folder16.ico") {
    PID = getRandomInt(100000)
    if (type == "ie") { // Eventually I'll probably have more window types...
        var encodedTarget = ("https://picsdev.universe.dog/?view=ie&target=" + encodeURI(target));
        Windows.insertAdjacentHTML('beforeend', tpl({ PID, title, url:encodedTarget, icon}));
    } else {
        Windows.insertAdjacentHTML('beforeend', tpl({ PID, title, url:target, icon}))
    }
    // Create the script for this window
    const s = document.createElement('script');
    s.src = `../assets/js/window.js?PID=${PID}`;
    document.body.appendChild(s);
}

// Spawn a window with JS
//spawn("ie", "Paint!", "https://nitripaint.com")