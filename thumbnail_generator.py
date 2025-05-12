# Thumbnail Generator
# Checks for and generates thumbnails for PicPile
# Daisy Universe [D]
# 05 . 11 . 25

from hashlib import md5
from PIL import Image 
import os

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

"""
example of a valid thumbs_db.json: 

{
    "./Follow.jpg": "09f52f4b1a7ff2993d049c9d9891522d",
    "./Friend.jpg": "09ccfe830cd4b56c6063ac70e93a7211",
    "./Ascent.jpg": "fc516fb6395f9fdbd26b89e8bf3aaea6",
    "./Radiance.jpg": "1cfcd0c0e00c208ca3b8685d5293f89c",
    "./Autumn.jpg": "7d57af950cfa3c4501b348772f98162c",
    "./Tulips.jpg": "191bd03fc0950c261beff4104e786f84",
    "./Vortec space.jpg": "da64f0317ffc818c0e96e8410994556b",
    "./bliss.jpg": "0b8d31bc5002df9ff0868269056c0a9a",
    "./Wind.jpg": "3015cbbd43396817a760815eaeafa42d",
    "./Azul.jpg": "e1ec0e4572c5ccb1a95571a98221a800",
    "subfolder/kamina.jpg": "ae29ce1035d16dca1b19f4a9a6dd9da3",
    "subfolder/son.jpg": "1d0b44f9408fb30cde5c1bc1de7cb77d",
    "_subfolder/kamina.jpg": "ae29ce1035d16dca1b19f4a9a6dd9da3",
    "_subfolder/son.jpg": "1d0b44f9408fb30cde5c1bc1de7cb77d"
}
"""