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
from flask_simple_captcha import CAPTCHA

SECRET_KEY = os.getenv("TEMPSECRET_KEY")

# Thanks:
# https://www.freecodecamp.org/news/how-to-build-a-web-application-using-flask-and-deploy-it-to-the-cloud-3551c985e492/

DEFAULT_CONFIG = {
    'SECRET_CAPTCHA_KEY': SECRET_KEY,
    'CAPTCHA_LENGTH': 6,  # Length of the generated CAPTCHA text
    'CAPTCHA_DIGITS': False,  # Should digits be added to the character pool?
    # EXPIRE_SECONDS will take prioritity over EXPIRE_MINUTES if both are set.
    'EXPIRE_SECONDS': 60 * 10,
    #'EXPIRE_MINUTES': 10, # backwards compatibility concerns supports this too
    #'EXCLUDE_VISUALLY_SIMILAR': True,  # Optional
    #'ONLY_UPPERCASE': True,  # Optional
    #'CHARACTER_POOL': 'AaBb',  # Optional
}

app = Flask(__name__, static_folder="static/")
# app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = os.urandom(24)
ALLOWED_EXTENSIONS = {".epw"}
app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path,"uploads")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
CORS(app)
SIMPLE_CAPTCHA = CAPTCHA(config=DEFAULT_CONFIG)
app = SIMPLE_CAPTCHA.init_app(app)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
@cross_origin(supports_credentials=True)
def home():
    return render_template("home.html", greetings="Hello, world!")


@app.route("/about")
@cross_origin(supports_credentials=True)
def about():
    return render_template("about.html")


@app.route("/morpher", methods=["GET", "POST"])
@cross_origin(supports_credentials=True)
def morpher():
    # https://help.pythonanywhere.com/pages/environment-variables-for-web-apps
    session.clear()
    if request.method == "POST":
        if request.files["epw-file"].filename == "":
            result_files = {"app": "morpher"}
            # change to error base don lack of file or make form validatable
            baseline = request.form.get('hidden-baseline-range').split(",")
            baseline = (int(baseline[0]),int(baseline[1])) 
            return jsonify(result_files)
        else:
            c_hash = request.form.get('captcha-hash')
            c_text = request.form.get('captcha-text')
            if SIMPLE_CAPTCHA.verify(c_text, c_hash):
                    
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
            else:
                return 'failed captcha'
            
    else:           
        new_captcha_dict = SIMPLE_CAPTCHA.create()
        
        return render_template("morpher.html", captcha=new_captcha_dict)

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
