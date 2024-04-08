# imports

from dotenv import load_dotenv, dotenv_values 
from flask import Flask, render_template, redirect, request, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from db_connection import cursor, conn
import os
from datetime import datetime


# FUNCTIONS
def current_date():
    return datetime.now().strftime("%Y-%m-%d")

# loading variables from .env file
load_dotenv()

# initialize the flask app
app: Flask = Flask(__name__)

# configs for Flask App
app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY")

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
        # return redirect(url_for("test", usr_data=usr_email))
        
    else:
        return render_template("Login.html")

@app.route("/<usr_data>")
def test(usr_data):
    return usr_data

@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        usr_name = request.form['name']
        usr_email = request.form['email']
        usr_pwd = request.form['password']
        sql = ("SELECT * FROM user_tbl WHERE email=%s")
        cursor.execute(sql, (usr_email, ))
        if len(cursor.fetchall()) < 1:
            # ready to insert data
            #hashing the password
            status = 1
            hashed_password = generate_password_hash(usr_pwd, "pbkdf2", 10)
            sql = "INSERT INTO user_tbl (name, email, password, date_added, status) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (usr_name, usr_email, hashed_password, current_date(), status))
            conn.commit()
            if cursor.rowcount == 1:
                return render_template("Login.html", success=f"{usr_name} Registered Successfully!")
            else:
                return render_template("Register.html", error="Error occurred while performing the operation")

        else:
            # usre already exists
            warning_message = f"{usr_email} alredy exists!"
            return render_template("Register.html", error=warning_message)

    else:
        return render_template("Register.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")