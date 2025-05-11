# PicPile
# Serve your images in a windows XP Filmstrip view
# Daisy Universe [D]
# 05 . 08 . 25

from flask import Flask, render_template, send_from_directory, abort, url_for, request
from markupsafe import Markup
from hashlib import md5
from PIL import Image 
import json
import os

app = Flask(__name__)

#-------- Utility functions --------#

# Load config from a json, allow us to get/set easily
class cfgmgr:
    def __init__(self, filepath):
        self.filepath = filepath
        self._data = self._load_config()

    def _load_config(self):
        try:
            with open(self.filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def get(self, key, default=None):
         return self._data.get(key, default)

    def set(self, key, value):
        self._data[key] = value
        self._save_config()
        
    def _save_config(self):
        with open(self.filepath, 'w') as f:
            json.dump(self._data, f, indent=4)

    def delete(self, key):
        if key in self._data:
            del self._data[key]
            self._save_config()
        else:
            print(f"Key '{key}' not found in config.")

#-------- Image Thumbnail Junk --------#

# We will keep track of the MD5 of each file to support image replacements
def CalcMD5(filepath):
    hasher = md5()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

# Use PIL to generate the thumbnail..
def GenerateThumbnail(src_path, thumb_dir, size):
    os.makedirs(thumb_dir, exist_ok=True)
    fn = os.path.basename(src_path)
    dst_path = os.path.join(thumb_dir, fn)
    with Image.open(src_path) as img:
        print(f"Generating thumbnail for {src_path} in {dst_path}...")
        img.thumbnail(size)
        img.save(dst_path, optimize=True, quality=85)

# Run this on each pageload to make sure we have a thumbnail for each image
# Catches edge cases where user has added pictures without restarting the server
def CheapCheck(subdir, pic_dir, thumb_dir, size):
    full_dir = os.path.join(pic_dir, subdir)
    for name in sorted(os.listdir(full_dir)):
        if name.startswith("_"):
            continue
        src = os.path.join(full_dir, name)
        if os.path.isdir(src):
            continue
        dst = os.path.join(thumb_dir, subdir, name)
        if not os.path.exists(dst):
            GenerateThumbnail(src, os.path.join(thumb_dir, subdir), size)

# Do a full scan of the entire pictures directory to build all thumbnails
# this one is a bit more expensive because we need to calculate the MD5 of each file
# so only do this once per restart...
def FullCheck(pic_dir, thumb_dir, size, thumbdb):
    # Track which files actually exist
    existing = set()

    # Walk through pics, generate/update thumbs
    for root, dirs, files in os.walk(pic_dir):
        rel_dir = os.path.relpath(root, pic_dir)
        for name in files:
            src = os.path.join(root, name)
            key = os.path.join(rel_dir, name)

            existing.add(key)

            checksum = CalcMD5(src)
            print(f"checking {key} MD5... \nMD5: [{checksum}]")

            if thumbdb.get(key) != checksum:
                print(f"{key} MD5 change detected! regenerating thumbnail")
                GenerateThumbnail(
                    src,
                    os.path.join(thumb_dir, rel_dir),
                    size
                )
                thumbdb.set(key, checksum)

    # Prune thumbdb entries for files that no longer exist
    for key in list(thumbdb._data.keys()):
        if key not in existing:
            print(f"{key} not found on disk! removing from thumbdb")
            # delete from thumbdb
            thumbdb.delete(key)
            # also remove the thumbnail file itself, if present
            thumb_path = os.path.join(thumb_dir, key)
            if os.path.exists(thumb_path):
                os.remove(thumb_path)
                print(f"  deleted thumbnail file: {thumb_path}")

#--------------------------------------#

BASE_DIR  = os.path.dirname( __file__ )
config    = cfgmgr( os.path.join( BASE_DIR, "config/config.json"  ) )
thumbdb   = cfgmgr( os.path.join( BASE_DIR, config.get("ThumbDB") ) )

# On server start, do a full thumbnail scan
print("FULLCHECK: Scanning for changes in picture MD5 hashes...")
FullCheck( config.get("PicturesDir"), 
    config.get("ThumbnailPath"), 
    tuple(config.get("ThumbnailSize", [128,128])),
    thumbdb )

#-------------- Endpoints -------------#

# Main endpoint to serve the file browser
@app.route("/", defaults={"subpath": ""})
@app.route("/<path:subpath>")
def index(subpath):
    title = config.get("Title")

    folder = os.path.join(config.get("PicturesDir"), subpath)
    
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

    return render_template("index.html", entries=entries, current_url=loc, title=title, folder=titlebar)

# Serve pictures (or thumbnails)
@app.route("/pictures/<path:filename>")
def pictures(filename): 
    thumb = request.args.get('Thumbnail', default = 'Yes', type = str)
    if thumb == 'Yes':
        return send_from_directory(config.get("ThumbnailPath"), filename)
    else:
        return send_from_directory(config.get("PicturesDir"), filename)

# Serve assets from da assets folder
@app.route("/assets/<path:filename>")
def assets(filename): return send_from_directory(config.get("AssetsDir"), filename)

if __name__ == "__main__": app.run(debug=config.get("Debug"), port=config.get("Port"), host=config.get("Host"))

