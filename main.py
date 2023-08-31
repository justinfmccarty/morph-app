from flask import Flask, render_template, request, session, make_response, send_file, Response
import zipfile
from flask_session import Session
import numpy as np
import io
import os
import pandas as pd
import time
import csv



# Thanks:
# https://www.freecodecamp.org/news/how-to-build-a-web-application-using-flask-and-deploy-it-to-the-cloud-3551c985e492/

app = Flask(__name__, static_folder="static/")
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = "my_session"# os.urandom(24)

SESSION_TYPE = "filesystem"
app.config.from_object(__name__)
Session(app)

@app.route("/")
def home():
    return render_template("home.html", greetings="Hello, world!")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/morpher")
def morpher():
    return render_template("morpher.html")


@app.route("/exec-get-cmip")
def get_cmip():
    # Your Python function code here
    df_dict = func1()
    return {"result": "success", "dataframe": df_dict}


def func1():
    print("Starting function")
    time.sleep(0.25)
    print("Creating array")
    time.sleep(0.25)
    arr = np.random.rand(1000, 7)
    print("Transfer array to dataframe")
    time.sleep(0.25)
    df = pd.DataFrame(arr).to_dict()
    session["data"] = df
    return df


@app.route("/exec-morph-epw")
def morph_epw():
    # Your Python function code here
    # df = func1()
    data = session["data"]
    df = pd.DataFrame(data)[[0,1,2,3]]
    print(df)
    session["data"] = df.to_dict()
    return {"result": "success"}


@app.route("/exec-get-results")
def get_results():
    csv = '1,2,3\n4,5,6\n'
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=myplot.csv"})

    
    
    
    


@app.route("/analysis")
def analysis():
    return render_template("analysis.html")


if __name__ == "__main__":
    app.run(debug=True)
