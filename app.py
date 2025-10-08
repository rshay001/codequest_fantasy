from flask import Flask, render_template, abort, request, redirect, url_for, session, flash, jsonify, Response
from pathlib import Path
import markdown
import json
import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

BASE = Path(__file__).parent
CHALLENGES_DIR = BASE / "challenges"
DATA_DIR = BASE / "data"
ANSWERS_FILE = DATA_DIR / "answers.json"
PROGRESS_FILE = DATA_DIR / "progress.json"

app = Flask(__name__)
app.secret_key = "replace-this-with-a-random-secret-for-production"

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///local.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
class UserProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    progress_data = db.Column(db.Text)  # Store JSON as text
    
class UserAnswers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    day = db.Column(db.Integer, nullable=False)
    answer = db.Column(db.String(200))

# Create tables (it's smart, so if the table exists, it won't recreate)
with app.app_context():
    db.create_all()


# Ensure data dir exists
DATA_DIR.mkdir(exist_ok=True)

# Load answers
if not ANSWERS_FILE.exists():
    # create a placeholder to avoid crashes; actual answers are included in repo
    ANSWERS_FILE.write_text(json.dumps({}, indent=2))

with open(ANSWERS_FILE) as f:
    ANSWERS = json.load(f)

# Load or init progress
if not PROGRESS_FILE.exists():
    PROGRESS_FILE.write_text(json.dumps({"users": {}}, indent=2))

def load_progress():
    with open(PROGRESS_FILE) as f:
        return json.load(f)

def save_progress(data):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/")
def index():
    # list available days
    days = sorted([p.stem for p in CHALLENGES_DIR.glob("day*.md")])
    user = session.get("username")
    progress = load_progress()
    user_data = progress.get("users", {}).get(user, {}) if user else None
    solved = set(user_data.get("solved", [])) if user_data else set()
    return render_template("index.html", days=days, user=user, solved=solved)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        if not username:
            flash("Please enter a name.")
            return redirect(url_for("login"))
        session["username"] = username
        # ensure user exists in progress
        progress = load_progress()
        users = progress.setdefault("users", {})
        users.setdefault(username, {"solved": [], "last_seen": None})
        users[username]["last_seen"] = datetime.utcnow().isoformat()
        save_progress(progress)
        return redirect(url_for("index"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))

@app.route("/day/<day>")
def day(day):
    file = CHALLENGES_DIR / f"{day}.md"
    if not file.exists():
        abort(404)
    raw = file.read_text()
    content = markdown.markdown(raw, extensions=['codehilite', 'fenced_code'])
    user = session.get("username")
    progress = load_progress()
    user_data = progress.get("users", {}).get(user, {}) if user else {}
    solved = set(user_data.get("solved", [])) if user else set()
    is_solved = day in solved
    return render_template("day.html", content=content, day=day, user=user, is_solved=is_solved)

@app.route("/submit/<day>", methods=["POST"])
def submit(day):
    username = session.get("username")
    if not username:
        flash("Please login first.")
        return redirect(url_for("login"))
    answer = request.form.get("answer", "").strip()
    if not answer:
        flash("Please enter an answer.")
        return redirect(url_for("day", day=day))
    correct = ANSWERS.get(day)
    if correct is None:
        flash("No answer configured for this day. Contact the admin.")
        return redirect(url_for("day", day=day))

    # simple string compare — you can enhance with number parsing, whitespace normalization, etc.
    normalized = answer.strip()
    if normalized == str(correct):
        # mark progress
        progress = load_progress()
        users = progress.setdefault("users", {})
        user_data = users.setdefault(username, {"solved": [], "last_seen": None})
        if day not in user_data.get("solved", []):
            user_data.setdefault("solved", []).append(day)
            user_data["last_seen"] = datetime.utcnow().isoformat()
            save_progress(progress)
        flash("✅ Correct! Star awarded.")
    else:
        flash("❌ Not quite. Try again!")
    return redirect(url_for("day", day=day))

@app.route("/api/progress")
def api_progress():
    # small API to fetch progress for UI or other uses
    progress = load_progress()
    return jsonify(progress)

@app.route("/input/<day>")
def get_input(day):
    input_file = BASE / "inputs" / f"{day}.txt"
    if not input_file.exists():
        abort(404)
    return Response(input_file.read_text(), mimetype='text/plain')



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True)