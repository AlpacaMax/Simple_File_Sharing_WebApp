import datetime
from flask import render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from werkzeug.wrappers import Response
from werkzeug.datastructures import Headers
from App import app, db
from App.models import File

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # print(request.files)
        if 'file' not in request.files:
            flash("No file part")
            return redirect(request.url)

        file = request.files['file']
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file:
            filename = secure_filename(file.filename)
            file_bytes = b''
            for byte in file: file_bytes += byte
            new_file = File(
                filename=filename, 
                file=file_bytes, 
                datetime_added=datetime.datetime.now()
            )
            db.session.add(new_file)
            db.session.commit()

    files = File.query.order_by(File.filename).all()
    return render_template("home.html", files=files)

@app.route("/download/<int:id>", methods=["GET"])
def download(id):
    the_file = File.query.get(id)

    if (the_file is None):
        flash("File does not exist!")
        return redirect(url_for("home"))

    headers = Headers()
    headers.add("Content-Disposition", "attachment", filename=the_file.filename)

    return Response(
        the_file.file, 
        headers=headers, 
        mimetype="application/octet-stream"
    )

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    the_file = File.query.get(id)

    if (the_file is None):
        flash("File does not exist!")
        return redirect(url_for("home"))

    db.session.delete(the_file)
    db.session.commit()

    return redirect(url_for("home"))