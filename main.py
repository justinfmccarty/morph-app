from flask import Flask, render_template, request, Response, send_file, make_response, jsonify, send_from_directory, session, redirect
import zipfile
import webbrowser

from flask_session import Session
from flask_cors import CORS, cross_origin
import numpy as np
import io
import os
import pandas as pd
import time
from math import sqrt
import csv
from utilities import read_epw
import localscripts as ls
import string
import random
from werkzeug.wsgi import FileWrapper
import glob


# Thanks:
# https://www.freecodecamp.org/news/how-to-build-a-web-application-using-flask-and-deploy-it-to-the-cloud-3551c985e492/

app = Flask(__name__, static_folder="static/")
# app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = os.urandom(24)
ALLOWED_EXTENSIONS = {".epw"}
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
CORS(app)



def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# SESSION_TYPE = "filesystem"
# app.config.from_object(__name__)
# Session(app)


@app.route("/")
@cross_origin(supports_credentials=True)
def home():
    return render_template("home.html", greetings="Hello, world!")


@app.route("/about")
@cross_origin(supports_credentials=True)
def about():
    return render_template("about.html")


# @app.route("/morpher", methods =["GET", "POST"])
# def morpher():
#     if request.method == "POST":
#         if request.files['epw-file'].filename == '':
#             pass
#         else:
#             df = read_epw(request.files['epw-file'])
#             print(df)
#             print(request.form.to_dict())


#     return render_template("morpher.html")


@app.route("/morpher", methods=["GET", "POST"])
@cross_origin(supports_credentials=True)
def morpher():
    print("morph hi")
    print(session)
    session.clear()
    print("session: ", session)
    if request.method == "POST":
        if request.files["epw-file"].filename == "":
            result_files = {"app": "morpher"}
            # change to error base don lack of file or make form validatable
            baseline = request.form.get('hidden-baseline-range').split(",")
            baseline = (int(baseline[0]),int(baseline[1])) 
            print(baseline)
            return jsonify(result_files)
        else:
            file_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=42))
            tmp_file = os.path.join(app.config["UPLOAD_FOLDER"], 
                                    f"tmp_{request.form.get('project-name')}_{file_name}.epw"
                                    )
            with open(tmp_file,'wb') as fp:
                data = request.files.get("epw-file").read()
                fp.write(data)
                
            configured_form_data = ls.intake_form(request.form, tmp_file)
            session['project_name'] = configured_form_data.project_name
            morphed_epw_dict = ls.morphing_workflow(configured_form_data)
            # returns an epw object (need to iterate and write to a zip archive for each of the three keys)            
            result_files = ls.write_result_epws(configured_form_data, morphed_epw_dict)
            for k,v in result_files.items():
                session[k] = v
        
            result_files = {"app": "morpher"}
            # TODO get redirect to work?
            # return redirect("/download-morph-results")
            return jsonify(result_files)
            
                
    return render_template("morpher.html")

@app.route("/download-morph-results")
@cross_origin(supports_credentials=True)
def get_results():

    fileobj = io.BytesIO()
    with zipfile.ZipFile(fileobj, 'w') as zip_file:
        zip_info = zipfile.ZipInfo("Archive2.zip")
        zip_info.date_time = time.localtime(time.time())[:6]
        zip_info.compress_type = zipfile.ZIP_DEFLATED
        for k,v in session.items():
            if ".epw" in k:
                zip_file.writestr(k, v)
    fileobj.seek(0)
    filename = f"morphed_{session['project_name']}.zip"
    session.clear()
    return Response(fileobj.getvalue(),
                    mimetype='application/zip',
                    headers={'Content-Disposition': f"attachment;filename={filename}"})

@app.route("/analysis")
@cross_origin(supports_credentials=True)
def analysis():
    return render_template("analysis.html")


if __name__ == "__main__":
    app.run(debug=True)
