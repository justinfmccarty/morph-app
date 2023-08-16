from flask import Flask, render_template
# Thanks: 
# https://www.freecodecamp.org/news/how-to-build-a-web-application-using-flask-and-deploy-it-to-the-cloud-3551c985e492/

app = Flask(__name__, static_folder="static/")

@app.route("/")
def home():
    return render_template("home.html", greetings="Hello, world!")

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/morpher")
def morpher():
    return render_template("morpher.html")


@app.route("/analysis")
def analysis():
    return render_template("analysis.html")


if __name__ == "__main__":
    app.run(debug=True)