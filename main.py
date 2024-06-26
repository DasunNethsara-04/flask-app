# imports
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, request, session, url_for, flash
from flask_bcrypt import Bcrypt
from db_connection import cursor, conn
from datetime import datetime
import os


# FUNCTIONS
def current_date() -> str:
    return datetime.now().strftime("%Y-%m-%d")

# loading variables from .env file
load_dotenv()

# initialize the flask app
app: Flask = Flask(__name__)
bcrypt:Bcrypt = Bcrypt(app)

# configs for Flask App
app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY")

# routers
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
        sql = "SELECT * FROM user_tbl WHERE email=%s"
        cursor.execute(sql, (usr_email, ))
        try:
            result = cursor.fetchone()
            if len(result) > 0:
                #user exists
                if bcrypt.check_password_hash(result[3], str(usr_pwd)):
                    session['EMAIL'] = usr_email
                    session['USER_ID'] = result[0]
                    session['IS_LOGGED_IN'] = True
                    return redirect(url_for("admin_dashboard"))
                else:
                    return render_template("Login.html", error="Invalid Password")
            else:
                # user not found
                return render_template("Login.html", error="User Not Found")
        except TypeError:
            return render_template("Login.html", error="User Not Found")
        
    else:
        return render_template("Login.html")

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
            role = "Admin"
            hashed_password = bcrypt.generate_password_hash(usr_pwd)
            sql = "INSERT INTO user_tbl (name, email, password, date_added, status, user_role) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (usr_name, usr_email, hashed_password, current_date(), status, role))
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

@app.route('/logout')
def logout():
    session.pop('EMAIL',None)
    session.pop('IS_LOGGED_IN',None)
    return redirect(url_for('login'))

@app.route("/admin")
def adminPage():
    return render_template("Pages/dashboard.html")

@app.route("/admin/dashboard")
def admin_dashboard():
    return render_template("Pages/dashboard.html")

@app.route("/admin/show-users")
def show_users():
    sql  = "SELECT * FROM user_tbl WHERE status=1 AND user_role='User'"
    cursor.execute(sql)
    return render_template("Pages/show_users.html", users=cursor.fetchall())

@app.route("/admin/add-user", methods=['POST', 'GET'])
def add_user():
    if request.method == 'POST':
        user_name = request.form['name']
        user_email = request.form['email']
        status = 1
        role = "User"
        sql = "SELECT COUNT(*) FROM user_tbl WHERE email=%s"
        cursor.execute(sql, (user_email, ))
        if int(cursor.fetchone()[0]) < 1:
            sql = "INSERT INTO user_tbl (name, email, date_added, status, user_role) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (user_name, user_email, current_date(), status, role))
            conn.commit()

            if cursor.rowcount == 1:
                flash(f"{user_name} registered successfully!")
            else:
                flash("Error occurred while performing the operation")
            return render_template("Pages/add-user.html")
        else:
            # already exists
            flash(f"{user_email} already exists")
        return render_template("Pages/add-user.html")
    else:
        return render_template("Pages/add-user.html")

@app.route("/admin/edit-user/<user_id>", methods=['POST', 'GET'])
def edit_user(user_id):
    if request.method == 'POST':
        user_name = request.form['name']
        user_email = request.form['email']
        sql = "UPDATE user_tbl SET name=%s, email=%s, date_updated=%s WHERE user_id='"+user_id+"'"
        cursor.execute(sql, (user_name, user_email, current_date()))
        conn.commit()
        if cursor.rowcount == 1:
            flash(f"{user_name} updated successfully!")
        else:
            flash("Error occurred while performing the operation")
        sql = f"SELECT * FROM user_tbl WHERE user_id='{user_id}'"
        cursor.execute(sql)
        return render_template("Pages/edit-user.html", user=cursor.fetchone())
    else:
        sql = f"SELECT * FROM user_tbl WHERE user_id='{user_id}'"
        cursor.execute(sql)
        return render_template("Pages/edit-user.html", user=cursor.fetchone())

@app.route("/admin/delete-user/<user_id>")
def delete_user(user_id):
    sql  = "UPDATE user_tbl SET status=0 WHERE user_id='"+user_id+"'"
    cursor.execute(sql)
    conn.commit()
    if cursor.rowcount == 1:
        flash(f"User deleted successfully!")
    else:
        flash("Error occurred while performing the operation")
    return redirect(url_for("show_users"))

@app.route("/admin/profile/<user_id>")
def profile(user_id):
    sql  = "SELECT * FROM user_tbl WHERE user_id='"+user_id+"'"
    cursor.execute(sql)
    return render_template("Pages/user-profile.html", user=cursor.fetchone())


# error handlers
@app.errorhandler(401)
def bad_request(err):
    return render_template("401.html"), 401

@app.errorhandler(404)
def page_not_found(err):
    return render_template("404.html"), 404

@app.errorhandler(500)
def server_error(err):
    return render_template("500.html"), 500


# run the Flask app
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
