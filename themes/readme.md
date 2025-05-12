# <center>Themes</center>
<br><br>
This folder basically contains all the logic, styling, and graphics resources for the entire project. I have tried to make each part of the site as modular as possible to allow for user customization

I recently added this concept of 'themes' which is basically a different way of saying that the assets folder is configurable and changable in runtime. If you decide that you want to make your own theme, it should be as easy as copying the Luna theme to it's own folder and modifying what you want inside of it. You should be able to modify the "Theme" value in your conifg.json to tell the server
to serve assets from that folder instead of the default 'Luna'

The hope is that people in the future are able to navigate this code and play with it, and perhaps even learn a little bit about web/server design in the process while creating something
that's tailored to their own particular brand of weirdo

The site is broken down into several components which I have tried to make fit together modularly to ease in tweaking small parts without breaking everything, they are as follows:

---

### TITLEBAR

The titlebar is just the topmost bar of the site containing the title and the bar. and also the WM controls!

```js
templates/titlebar.html
themes/luna/css/titlebar.css
themes/luna/js/titlebar.js
```

---

### MENUBAR

Menubar contain the collapsable menu system near the top of the window (File, Edit, View, etc.,)
Currently I am in the process of making it so that the menubar is dynamically generated from menubar.json, this is being prototyped but is not yet fully
implemented. The hope is for eventually the server owner can simply list out any of their desired custom content in there, and define where they want
that to take the user, or even define a callback to a custom function in menubar.js

Where the menubar is generated, not meant to be directly modified:
```js
templates/menubar.html
```

The CSS is largely responsible for the logic of the collapsing menus, so be careful with how you mess with this one because it's a bit.. fiddly.
```js
themes/luna/css/menubar.css
```

Will contain functions that you will want to call back with the menubar
```js
themes/luna/js/menubar.js
```

---
### NAVBAR

The Navbar is the header ribbon containing things like the file navigation buttons and the address bar

```js
templates/navbar.html
themes/luna/css/navbar.css
themes/luna/js/navbar.js
```

---
<br><br>
# <center>Views</center>
<br><br>
Views are prefabs of the content of the window for a given view (think Filmstrip, Thumbnails, List, etc.,)
For now the only implemented view is Filmstrip as that is the primary end goal of this project, but this system will eventually allow for all
of the actual windows file explorer fileviews

Currently the default view is defined in the config/config.json as "DefaultView", but this can be over-ridden by the user by defining a 'view' url parameter
Eventually this will allow users to choose different views from both the navbar and the menubar to change how the images are presented.

Views exist in a fixed structure and can be replicated in much the same was that themes can, by simply creating a new folder and setting the folder name
in the config or the url param, all content for Actions and Content will be served from those folders instead

## Filmstrip

Filmstrip view is the primary view of PicPile as it was developped with the intention of recreating this particular folder view. it presents all of your images
as thumbnails in a reel on the bottom pane of the site, with a large central image preview. It also contains a side-bar for 'Actions' for doing what would
have been common tasks on a computer of the time.

---
### ACTIONS

Actions contains the whole of the left-most pane, which has all of the 'action task' windows (Picture Tasks, File and Folder Tasks, etc)
As of right now, this is static and doesn't even really do much other than link back to my home site as a placeholder, but eventually
I am going to implement a system for defining your own actions pane, with top level 'windows' and secondary 'tasks'

This is the reason for keeping a dedicated js file for this section, as eventually I would like to make it so that a user defined action can simply
define a function that it can call back from that script.

```js
templates/actions.html
themese/luna/css/actions.css
themes/luna/js/actions.js
```

---
### CONTENT

This contains the main image preview, along with the filmreel. A lot of this is dynamically generated, so it's not condusive to direct modification, but it's there if you want to mess with it

```js
templates/views/filmreel/content.html
themese/luna/css/views/filmreel/content.css
themes/luna/js/views/filmreel/content.js
```

---
### MISC HANDLERS

These are all little files that handle the rest of the edge cases that are too small to justify turning into their own section

---
Styles the site before everything else, mostly just to setup common stuff and utility classes
```js
themes/luna/css/style.css
```
---
Responsible for styling the mobile version of the site
```js
themes/luna/css/mobile.css
```
---
This is the main container for the entire site, but it's mostly just a skeleton that breaks out all of the other sections with jinja
```js
templates/index.html
```
---
This contains the html <head> stuff, including calling all of the stylesheets. If you want to make a custom embed, you'd put it in here
```js
templates/header.html
```
---
