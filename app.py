from flask import Flask, render_template, abort, request, redirect, url_for, session, flash, jsonify, Response
from pathlib import Path
import markdown
import json
import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

#File paths (for challenges)
BASE = Path(__file__).parent
CHALLENGES_DIR = BASE / "challenges"
DATA_DIR = BASE / "data"
ANSWERS_FILE = DATA_DIR / "answers.json"

app = Flask(__name__)
app.secret_key = "replace-this-with-a-random-secret-for-production"

#========== Database setup ===========
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///local.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
class UserProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    progress_data = db.Column(db.Text)  # Store JSON as text


# Create tables (it's smart, so if the table exists, it won't recreate)
with app.app_context():
    db.create_all()

def check_user(username):
    existing_user = UserProgress.query.filter_by(username=username).first()
    if not existing_user:
        new_user = UserProgress(username=username, progress_data=json.dumps({"solved": [], "last_seen": None}))
        db.session.add(new_user)
        db.session.commit()
        return True #user created
    return False #user already exists

def save_user_progress(progress_dict):
    username = session.get("username")
    if not username:
        return
    user = UserProgress.query.filter_by(username=username).first()
    if user:
        user.progress_data = json.dumps(progress_dict)
    else: #has a username but no record. Create one.
        user = UserProgress(username=username, progress_data=json.dumps(progress_dict))
        db.session.add(user)
    db.session.commit()

def load_user_progress():
    username = session.get("username")
    if not username:
        return {"solved": [], "last_seen": None}
    user = UserProgress.query.filter_by(username=username).first()
    if user and user.progress_data:
        return json.loads(user.progress_data)
    return {"solved": [], "last_seen": None}

def mark_day_solved(day):
    progress = load_user_progress()
    if day not in progress.get("solved", []):
        progress.setdefault("solved", []).append(day)
        progress["last_seen"] = datetime.now().isoformat() #isoformat for JSON serialization
        save_user_progress(progress)


#========== App Stuff ==========
@app.route("/")
def index():
    # list available days
    days = sorted([p.stem for p in CHALLENGES_DIR.glob("day*.md")])
    user = session.get("username")
    progress = load_user_progress()
    solved = set(progress.get("solved", []))
    return render_template("index.html", days=days, user=user, solved=solved)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        if not username:
            flash("Please enter a name.")
            return redirect(url_for("login"))
        
        session["username"] = username
        check_user(username)
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
    progress = load_user_progress()
    solved = set(progress.get("solved", []))
    is_solved = day in solved
    return render_template("day.html", content=content, day=day, user=user, is_solved=is_solved)

@app.route("/submit/<day>", methods=["POST"])
def submit(day):
    username = session.get("username")
    if not username:
        flash("Please login first.")
        return redirect(url_for("login"))
    user_answer = request.form.get("answer", "").strip()
    if not user_answer:
        flash("Please enter an answer.")
        return redirect(url_for("day", day=day))
    with open(ANSWERS_FILE) as f:
        answers = json.load(f) #all days' answers, not just today's

    correct_answer = answers.get(day)
    if correct_answer is None:
        flash("No answer configured for this day. Contact the admin.")
        return redirect(url_for("day", day=day))

    if user_answer == str(correct_answer):
        # mark progress
        mark_day_solved(day)
        flash("✅ Correct! Star awarded.")
    else:
        flash("❌ Not quite. Try again!")
    return redirect(url_for("day", day=day))

@app.route("/api/progress")
def api_progress():
    # small API to fetch progress for UI or other uses
    progress = load_user_progress()
    return jsonify(progress)

@app.route("/input/<day>")
def get_input(day):
    input_file = BASE / "inputs" / f"{day}.txt"
    if not input_file.exists():
        abort(404)
    return Response(input_file.read_text(), mimetype='text/plain')



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True)