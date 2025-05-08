# PicPile
# A Simple flask server that shows your images in a Windows XP filmstrip view
# Daisy Universe [D]
# 05 . 05 . 25

from flask import Flask, render_template, request, redirect, Response, send_from_directory, url_for, send_file, make_response, jsonify
import os

app = Flask(__name__)

# Allowed file extensions
imageExtensions = {'.png', '.jpg', '.jpeg', '.gif'}

#------------------------------------------------------------#
#                      Endpoints                             #
#------------------------------------------------------------#

@app.route('/<path:sub_path>')
def picpile(sub_path):
    # if the request ends in a file extension, serve the requested image
    if request.url.endswith(imageExtensions)
        return make_response( send_file( ( "/pictures/" + sub_path ) ) )
    else :
        # If the request is just a directory, render the filmstrip
        files = listdir(( "/pictures/" + sub_path ))
        thumbnails = generateThumbnails(files)
        
        return render_template {
            "index.html",
            thumbnails = thumbnails
        }

#------------------------------------------------------------#
#                  Utility Functions                         #
#------------------------------------------------------------#

# Generate a list of thumbnails from a list of filepaths
def generateThumbnails(files):
    thumbnails = [] 
    for file in files:
        filename = file.split("/")[-1].split(".")[0]
        thumbnail = ('<div class="thumbnail"><img src="' + file + '" width="16" height="16"><p>' + filename + '</p></div>\n')
        thumbnails.append(thumbnail)

    return thumbnails

# Get a list of filepaths from a given directory
def listDirectory(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

