
from flask import Flask, render_template, request, redirect, url_for, session
import json, os

app = Flask(__name__)
app.secret_key = "your_secret_key"

USERNAME = "admin"
PASSWORD = "1234"
DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == USERNAME and request.form["password"] == PASSWORD:
            session["logged_in"] = True
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if not session.get("logged_in"):
        return redirect("/")
    data = load_data()
    if request.method == "POST":
        new_entry = request.form.get("entry")
        if new_entry:
            data.append({"entry": new_entry})
            save_data(data)
            return redirect("/dashboard")
    return render_template("dashboard.html", data=data)

@app.route("/delete/<int:index>")
def delete(index):
    if not session.get("logged_in"):
        return redirect("/")
    data = load_data()
    if 0 <= index < len(data):
        data.pop(index)
        save_data(data)
    return redirect("/dashboard")

@app.route("/logout")
def logout():
    session["logged_in"] = False
    return redirect("/")

if __name__ == "__main__":
    app.run()
