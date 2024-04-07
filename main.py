from flask import Flask, render_template

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

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")