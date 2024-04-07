# imports
from flask import Flask, render_template, redirect, request, url_for

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

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        usr_email = request.form['email']
        usr_pwd = request.form['password']
        print(usr_email, usr_pwd)
        # return redirect(url_for("test", usr_data=usr_email))
    else:
        return render_template("Login.html")

@app.route("/<usr_data>")
def test(usr_data):
    return usr_data
@app.route("/register")
def register():
    return render_template("Register.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")