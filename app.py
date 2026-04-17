import json
from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__, template_folder="templates")

# Temporary users
users = {
    "administrator": [{"username": "admin", "password": "123"}],
    "manager": [{"username": "manager1", "password": "123"}],
    "employee": [{"username": "employee1", "password": "123"}]
}

# Jobs file path
JOBS_FILE = "jobs.json"

# Load jobs from file
def load_jobs():
    try:
        with open(JOBS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Save jobs to file
def save_jobs(jobs):
    with open(JOBS_FILE, "w") as f:
        json.dump(jobs, f)

# Store logged in user info
logged_in_user = {"role": None, "username": None}

@app.route("/")
def home():
    return render_template("signup.html")  # or login page
@app.route("/logout", methods=["POST"])
def logout():
    logged_in_user["role"] = None
    logged_in_user["username"] = None
    return redirect(url_for("home"))

@app.route("/login/<role>", methods=["POST"])
def login(role):
    username = request.form.get("username")
    password = request.form.get("password")

    for user in users.get(role, []):
        if user["username"] == username and user["password"] == password:
            logged_in_user["role"] = role
            logged_in_user["username"] = username
            return redirect(url_for("dashboard"))
    
    return f"Invalid credentials for {role.capitalize()}."

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    role = logged_in_user["role"]
    if not role:
        return redirect(url_for("home"))

    jobs = load_jobs()  # load jobs from file

    if request.method == "POST":
        action = request.form.get("action")
        job_title = request.form.get("job_title")
        job_index = request.form.get("job_index")

        if action == "add" and role in ["administrator", "manager"]:
            jobs.append(job_title)
        elif action == "edit" and role in ["administrator", "manager"]:
            jobs[int(job_index)] = job_title
        elif action == "delete" and role == "administrator":
            jobs.pop(int(job_index))

        save_jobs(jobs)  # save updated jobs to file

    return render_template("dashboard.html", jobs=jobs, role=role)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))