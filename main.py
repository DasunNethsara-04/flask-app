# imports
from flask import Flask, render_template

# initialize the flask app
app: Flask = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about_us():
    return render_template("AboutUs.html")

@app.route("/contact")
def contact_us():
    return render_template("Contact.html")

@app.route("/login")
def login():
    return render_template("Login.html")

@app.route("/register")
def register():
    return render_template("Register.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")