# PicPile
# Serve your images in a windows XP Filmstrip view
# Daisy Universe [D]
# 05 . 08 . 25

import os
from flask import Flask, render_template, send_from_directory, abort, url_for, request
from markupsafe import Markup

app = Flask(__name__)

# Setup directories, if you want to rename them, change that here first.. 
# This *should* technically allow for inserting an arbitrary path for images, if you want your pictures folder be a shared folder
BASE_DIR     = os.path.dirname(__file__)

PICTURES_DIR = os.path.join(BASE_DIR, "pictures")

ASSETS_DIR   = os.path.join(BASE_DIR, "assets")
FONTS_DIR    = os.path.join(ASSETS_DIR, "fonts")
GFX_DIR    = os.path.join(ASSETS_DIR, "gfx")

# Eventually allow for hot-swappable stylesheets/scripts for themes
STYLE        = "/css/style.css"
SCRIPT        = "/js/script.js"


# Main endpoint to serve the file browser
@app.route("/", defaults={"subpath": ""})
@app.route("/<path:subpath>")
def index(subpath):
    # ls
    folder = os.path.join(PICTURES_DIR, subpath)
    # Don't let users navigate to files
    if not os.path.isdir(folder):
        abort(404)

    # Generate the folder based on contents per page load so we don't have to reload the server to add more content
    entries = []
    for name in sorted(os.listdir(folder)):
        # Don't show files/folders that start with "_" 
        # (allows for subfolders that can only be reached via direct link)
        if name.startswith("_"): continue

        rel = f"{subpath}/{name}" if subpath else name
        loc = ( request.url )
        # Get just the name for labelling purposes
        name_only = os.path.splitext(name)[0]
        entries.append({
            "name": name,
            "label": name_only,
            "path": rel,
            "is_dir": os.path.isdir(os.path.join(folder, name))
        })

    return render_template("index.html", entries=entries, current_url=loc, stylesheet=STYLE, js=SCRIPT)

# Serve the actual pics from the pictures directory
@app.route("/pictures/<path:filename>")
def pictures(filename):
    return send_from_directory(PICTURES_DIR, filename)

# Serve the graphics (icons and junk)
@app.route("/gfx/<path:filename>")
def assets(filename):
    return send_from_directory(GFX_DIR, filename)

# Serve some assets that would normally be static
# (mostly so I don't have to fight caching to do dev, will make it static later)
@app.route("/css/<path:filename>")
def style(filename): return send_from_directory(ASSETS_DIR, filename)

@app.route("/js/<path:filename>")
def script(filename): return send_from_directory(ASSETS_DIR, filename)

# Serve the fonts
@app.route("/fonts/<path:filename>")
def fonts(filename):
    return send_from_directory(FONTS_DIR, filename)

# Serve the favison
@app.route("/favicon.ico")
def favicon():
    return assets("favicon.ico")

if __name__ == "__main__":
    app.run(debug=True, port=420)
