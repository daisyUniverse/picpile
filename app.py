# PicPile
# Serve your images in a windows XP Filmstrip view
# Daisy Universe [D]
# 05 . 08 . 25

#---------------- Setup ---------------#

# 3rd party stuff
from flask import Flask, render_template, send_from_directory, abort, url_for, request
from markupsafe import Markup
import json
import os

# My stuff
import thumbnail_generator
import config_manager

app = Flask(__name__)

# initialize the config managers for site config, thumbnail md5 database, and theme selection
BASE_DIR  = os.path.dirname( __file__ )
config    = config_manager.cfgmgr( os.path.join( BASE_DIR, "config/config.json"  ) )
thumbdb   = config_manager.cfgmgr( os.path.join( BASE_DIR, config.get("ThumbDB") ) )
menubar   = config_manager.cfgmgr( os.path.join( BASE_DIR, config.get("Menubar") ) )
themedir  = os.path.join("themes", config.get("Theme"))

# @TODO: Currently, I think that setting the pictures folder in the config will only work on relative paths, this needs to be looked at..

# On server start, do a full thumbnail scan
print("FULLCHECK: Scanning for changes in picture MD5 hashes...")
thumbnail_generator.FullCheck( 
    config.get("PicturesDir"), 
    config.get("ThumbnailPath"), 
    tuple(config.get("ThumbnailSize", [128,128])),
    thumbdb 
)

#-------------- Endpoints -------------#

# Main endpoint to serve the file browser
@app.route("/", defaults={"subpath": ""})
@app.route("/<path:subpath>")
def index(subpath):
    title = config.get("Title")
    menubar_json = menubar.load()

    # Allow for custom view selection based on url param, with filmstrip as the configured default
    view = request.args.get('view', default = config.get("DefaultView"), type = str)
    
    folder = os.path.join(config.get("PicturesDir"), subpath)

    # Do a thumbnail cheapcheck on pageload
    thumbnail_generator.CheapCheck( 
        subpath, 
        config.get("PicturesDir"), 
        config.get("ThumbnailPath"), 
        tuple(config.get("ThumbnailSize", [128,128])) 
    )
        
    # Don't let users navigate to files
    if not os.path.isdir(folder):
        abort(404)

    loc = ( request.url )
    titlebar = loc.split("/")[-1]
    if titlebar == "": titlebar = title

    # Generate the folder based on contents per page load so we don't have to reload the server to add more content
    entries = []
    for name in sorted(os.listdir(folder)):
        
        # Don't show files/folders that start with "_" 
        # (allows for subfolders that can only be reached via direct link)
        if name.startswith("_"): continue

        # Get just the name for labelling purposes
        name_only = os.path.splitext(name)[0]
        rel = f"{subpath}/{name}" if subpath else name
        
        entries.append({
            "name": name,
            "label": name_only,
            "path": rel,
            "is_dir": os.path.isdir(os.path.join(folder, name))
        })

    return render_template("index.html", entries=entries, current_url=loc, title=title, folder=titlebar, view=view, menubar=menubar_json)

# Serve pictures (or thumbnails) based on url params
@app.route("/pictures/<path:filename>")
def pictures(filename): 
    thumb = request.args.get('Thumbnail', default = 'Yes', type = str)
    if thumb == 'Yes':
        return send_from_directory(config.get("ThumbnailPath"), filename)
    else:
        return send_from_directory(config.get("PicturesDir"), filename)

# Serve assets from da assets folder
@app.route("/assets/<path:filename>")
def assets(filename): 
    
    return send_from_directory(themedir, filename)

if __name__ == "__main__": app.run(debug=config.get("Debug"), port=config.get("Port"), host=config.get("Host"))

