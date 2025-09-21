# PicPile Config

PicPile is configured through a series of json files in this folder, here's what all their values mean:

# config.json

```json
{
    "PicturesDir"   : "pictures",
    "Theme"         : "luna",
    "DefaultView"   : "filmstrip",
    "ThumbDB"       : "config/thumbs_db.json",
    "Menubar"       : "config/menubar.json",
    "Actions"       : "config/actions.json",
    "Desktop"       : "config/desktop.json",
    "Wallpaper"     : "bliss.jpg",
    "Title"         : "PicPile",
    "BaseURL"       : "https://picsdev.universe.dog",
    "ThumbnailSize" : [128, 128],
    "ThumbnailPath" : "thumbs",
    "Debug"         : true,
    "Port"          : 420,
    "Host"          : "0.0.0.0"
}
```

## PicturesDir: 
The folder that your pictures will be served from. Currently only set up to work as a relative path

## Theme: 
The default theme to load all assets from. check /themes/readme.md for more information

## DefaultView: 
The default view to serve the actions and content sections from. Changing or creating these can modify the presentation or functionality of the site, and the view can be changed by the user with a URL parameter ( example: ?view=thumbnail )

## ThumbDB: 
This is the file where the thumbnail MD5 database is stored. Can be configured in case you want to run the same server for different instances

## Menubar: 
Changes what config file to load for the menubar content, basically the same as above, but also allows for dynamically loading different menubar contents depending on context or view

## Actions: 
Ditto for above but for the actions view. More on those later...

## Desktop: 
Location of the config containing all of the shortcuts available on the desktop view of the site

## Wallpaper: 
Changes the image that loads into the background of the desktop view, also controls the 'default' image that is first loaded in picpiles
preview. By default this is just an image from the relative path of your PicturesDir

## Title: 
Just changes the title of the site in various places to allow for more specific branding

## BaseURL:
Lets the server know what page to load from the desktop for internal page iframes (ie opening a picpile window)

## ThumbnailSize: 
Just changes the size of the thumbnails that are generated

## ThumbnailPath: 
Same as the PicturesDir but for thumbnails

## Debug: 
Lets you switch flask into debug mode for testing

Port: Port

Host: Host

# actions.json

```json
{
    "Picture Tasks" : {
        "Get pictures from Camera or Scanner"   : [ "camera.ico",       "https://daisy.universe.dog" ],
        "View as a Slide Show"                  : [ "project16.ico",    "https://daisy.universe.dog" ],
        "Order Prints Online"                   : [ "webphoto16.ico",   "https://daisy.universe.dog" ],
        "Print this picture"                    : [ "print16.ico",      "https://daisy.universe.dog" ],
        "Set as Desktop Background"             : [ "wallpaper16.ico",  "https://daisy.universe.dog" ],
        "Copy to CD"                            : [ "copycd16.ico",     "https://daisy.universe.dog" ],
        "Shop for pictures online"              : [ "webphoto16.ico",   "https://daisy.universe.dog" ]
    },
    "File and Folder Tasks" : {
        "Rename this file"                      : [ "rename.ico",       "https://daisy.universe.dog" ],
        "Move this file"                        : [ "move16.ico",       "https://daisy.universe.dog" ],
        "Copy this file"                        : [ "copy.ico",         "https://daisy.universe.dog" ],
        "Publish this file to the Web"          : [ "publish16.ico",    "https://daisy.universe.dog" ],
        "E-Mail this file"                      : [ "delete16.ico",     "https://daisy.universe.dog" ],
        "Shop for pictures online"              : [ "delete16.ico",     "https://daisy.universe.dog" ]
    },
    "Other Places" : {
        "Shared Pictures"                       : [ "picfolder16.ico",  "https://daisy.universe.dog" ],
        "My Pictures"                           : [ "picfolder16.ico",  "https://daisy.universe.dog" ],
        "My Computer"                           : [ "folder16.ico",     "https://daisy.universe.dog" ],
        "My Network Places"                     : [ "folder16.ico",     "https://daisy.universe.dog" ]
    },
    "Details" : {}
}
```
The actions json describes the content available in the 'actions' menu on the far left of the window.
For now, all it is, is a simple list of links, but you can make call backs to javascript if you want to
The structure is pretty simple. Pane title, pane items, and each pane item has an array, the first item of the array is the desired icon,
and the second item is the desired target. The first pane is always designated as the 'hero' pane, and is styled a bit differently

The details pane is not currently done, but will eventually demonstrate dynamic content

# desktop.json

```json
{
    "My Photos" :   {
        "name"      : "My Photos",
        "icon"      : "folders.png",
        "target"    : "https://picsdev.universe.dog",
        "type"      : "app"
    },
    "Nitripaint" :   {
        "name"      : "Nitripaint by nue",
        "icon"      : "favicon.ico",
        "target"    : "https://nitripaint.com",
        "type"      : "ie"
    },
    "The Flowerbed" :   {
        "name"      : "The Flowerbed",
        "icon"      : "daisy.png",
        "target"    : "https://daisy.universe.dog",
        "type"      : "ie"
    }
}
```

This is simply the list of desktop icons available in the desktop mode. 

## Name:
The title of the shortcut seen on the desktop

## Icon:
The filename of the icon relative to the /theme/<theme>/gfx/ path

## Target:
The target url - For now, each window is an iframe, so this only supports urls for now, but eventually I would like to make it so you
can invoke WASM stuff from here

## Type:
This is the type of window that's opened. For now there are only two types, "IE" and "App"
"IE" opens the URL in an IE6 style view, surrounding the content with the PicPile menubar, navbar, and address bar
"App" opens the URL in a pure iframe, only surrounding the window with the basic window decoration.

# menubar.json

```json
{
    "File" : {
        "New"               : ""
    },
    "Edit" : {
        "Undo Delete"           : "",
        "Seperator_0"           : "",
        "Cut"                   : ""
    },
    "View" : {
        "Seperator_0"   : "",
        "Filmstrip"     : "?view=filmstrip",
        "Falin"         : "?view=falin",
        "Seperator_1"   : "",
        "Arrange Icons By" : {
            "Name"              : false,
            "Align to Grid"     : false
        },
        "Seperator_2"               : "",
        "Refresh"                   : ""
    },
    "Favorites" : {
        "Add to Favorites..."       : "",
        "Orginize Favorites..."     : "",
        "Seperator_0"               : "",
        "Friends Websites" : {
            "Autumn Rain"       : "",
            "Nitripaint"        : "https://nitripaint.com"
        },
        "Daisies Websites" : {
            "Main Website"      : "https://universe.dog/",
            "Github"            : "https://github.com/daisyUniverse"
        }
    },
    "Tools" : {
        "Map Network Drive..."          : "",
        "Folder Options..."             : ""
    },
    "Help" : {
        "Help and Support Center"           : "",
        "About PicPile"                     : "https://github.com/daisyUniverse/picpile"
    }
}
```

(this is a very stripped down example)

The menubar json is responsible for generating the entire contents of the menubar. there are a few notes about how this works..
Each section can have an arbitrary number of subsections denoted by child objects. Each node containing a child will be shown as you would 
expect to see in windows...

Elements that are given a bool as it's value will be 'checkbox' type menubar items
Seperators can be designated by simply making an item starting with the word "Seperator_" and giving it an empty string as it's value
Javascript can be called using the same method as in the actions.json