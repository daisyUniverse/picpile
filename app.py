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

    return render_template("index.html", entries=entries, current_url=loc)

# Serve pictures from the pictures folder (user definable, so it needs to be seperate)
@app.route("/pictures/<path:filename>")
def pictures(filename): return send_from_directory(PICTURES_DIR, filename)

# Serve assets from da assets folder
@app.route("/assets/<path:filename>")
def assets(filename): return send_from_directory(ASSETS_DIR, filename)

if __name__ == "__main__": app.run(debug=True, port=420)
