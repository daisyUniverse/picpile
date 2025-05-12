# Themes

This repo basically contains all the logic, styling, and graphics resources for the entire project. I have tried to make each part of the site as modular as possible!

I recently added this concept of 'themes' which is basically a different way of saying that the assets folder is configurable. If you decide that you want to make your own theme, it should be as easy as copying the Luna theme to it's own folder and modifying what you want inside of it. As long as your 'Theme' config matches the name of the folder, PicPile will serve all assets from that folder instead of the default Luna folder.

The idea is that you don't have to muck about too much with the base install to make big changes

I should say there is a certain structure to everything in here, but I try to keep it consistant between all of the different parts of the site (CSS, JS, and Templates)

[Titlebar]

The titlebar is just the topmost bar of the site containing the title and the bar. and also the WM controls!

/templates/titlebar.html
css/titlebar.css
js/titlebar.js

[Menubar]

Menubar contain the collapsable menu system near the top of the window (File, Edit, View, etc.,)

(
    PS: 
    I realize that this is a wonderful place to place a 'link tree' of tons of different user-defined urls, since the aim of this is to be a kind of personal portfolio
    I don't want to lock this down behind some really weirdly written html, so...
    This is meant to eventually become completely modular and customizable, being defined by a prototype 'menubar.json' in the config folder
)

/templates/menubar.html
 - Where the menubar is generated, not meant to be directly modified
css/menubar.css
 - The CSS is largely responsible for the logic of the collapsing menus, so be careful with how you mess with this one because it's a bit.. fiddly.
js/menubar.js
 - Will contain functions that you will want to call back with the menubar



[Navbar]

The Navbar is the header ribbon containing things like the file navigation buttons and the address bar

/templates/navbar.html
css/navbar.css
js/navbar.js

[Actions]

Actions contains the whole of the left-most pane, which has all of the 'action task' windows (Picture Tasks, File and Folder Tasks, etc)

(
    PS: This to me also feels like it would a good place to allow users to drop their own links and content. There is a prototype of a 'actions.json' that I have yet to implement... 
    It will basically work like the Menubar.json, except this one takes two strings, one is a reference to an icon from gfx, and the other is what you want it to do. you can either user <script> tags in this to make it call a function in
    actions.js, or you can simply put a link in to make it link to some static content
)

/templates/actions.html
css/actions.css
js/actions.js

[Content]

This contains the main image preview, along with the filmreel. A lot of this is dynamically generated, so it's not condusive to direct modification, but it's there if you want to mess with it

/templates/content.html
css/content.css
js/content.js

[Misc Handlers]

These are all little files that handle the rest of the edge cases that are too small to justify turning into their own section

css/style.css
 - Styles the site before everything else, mostly just to setup common stuff and utility classes
css/mobile.css
 - Responsible for styling the mobile version of the site
templates/index.html
 - This is the main container for the entire site, but it's mostly just a skeleton that breaks out all of the other sections with jinja
templates/header.html
 - This contains the html <head> stuff, including calling all of the stylesheets. If you want to make a custom embed, you'd put it in here