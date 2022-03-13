from flask import Blueprint, render_template, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename

import os

views = Blueprint("views", __name__)

# Upload folder
UPLOAD_FOLDER = "website/uploads"

# List of image extensions
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

# Check if the file extension is allowed
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@views.route("/", methods=["GET", "POST"])
@views.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("home.html")
    elif request.method == "POST":
        print("here")
        # check if the post request has the file part
        if "file" not in request.files:
            print("No file part")
            return redirect(request.url)

        # get the file
        file = request.files["file"]

        # if user does not select file, browser also submit a empty part without filename
        if file.filename == "":
            print("No selected file")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return send_file(os.path.join("uploads/" + filename))
