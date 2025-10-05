# CodeQuest — Fantasy Adventure (30 days)

This project contains a ready-to-run local Flask app for a 30-day beginner "Advent of Code"-style challenge with separate usernames and progress tracking.

---

## File tree

```
codequest/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   ├── answers.json
│   └── progress.json
├── challenges/
│   ├── day01.md
│   ├── day02.md
│   └── ...
│   └── day30.md
├── templates/
│   ├── layout.html
│   ├── index.html
│   └── day.html
└── static/
    └── style.css
```

---

## app.py

```python
from flask import Flask, render_template, abort, request, redirect, url_for, session, flash, jsonify
from pathlib import Path
import markdown
import json
import os
from datetime import datetime

BASE = Path(__file__).parent
CHALLENGES_DIR = BASE / "challenges"
DATA_DIR = BASE / "data"
ANSWERS_FILE = DATA_DIR / "answers.json"
PROGRESS_FILE = DATA_DIR / "progress.json"

app = Flask(__name__)
app.secret_key = "replace-this-with-a-random-secret-for-production"

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
    days = sorted([p.name for p in CHALLENGES_DIR.glob("day*.md")])
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
    content = markdown.markdown(raw)
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
```

---

## templates/layout.html

```html
<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <title>CodeQuest — Fantasy Adventure</title>
    <link rel="stylesheet" href="/static/style.css" />
  </head>
  <body>
    <header>
      <h1><a href="/">CodeQuest — Fantasy Adventure</a></h1>
      <nav>
        {% if user %}
          <span>Logged in as <strong>{{ user }}</strong></span>
          <a href="/logout">Logout</a>
        {% else %}
          <a href="/login">Login</a>
        {% endif %}
      </nav>
    </header>
    <main>
      {% with messages = get_flashed_messages() %}
        {% if messages %}
          <ul class="flashes">
            {% for m in messages %}
              <li>{{ m }}</li>
            {% endfor %}
          </ul>
        {% endif %}
      {% endwith %}

      {% block body %}{% endblock %}
    </main>
    <footer>
      <small>Local test server — run with <code>python app.py</code></small>
    </footer>
  </body>
</html>
```

---

## templates/index.html

```html
{% extends "layout.html" %}
{% block body %}
  <h2>Challenges</h2>
  <p>Open a day to read the story and submit an answer.</p>
  <ul class="days">
    {% for d in days %}
      <li>
        <a href="/day/{{ d }}">{{ d|capitalize }}</a>
        {% if d in solved %}
          <span class="star">⭐</span>
        {% endif %}
      </li>
    {% endfor %}
  </ul>
{% endblock %}
```

---

## templates/login.html

```html
{% extends "layout.html" %}
{% block body %}
  <h2>Login</h2>
  <form method="post">
    <label>Choose a username (no password):</label>
    <input name="username" required />
    <button type="submit">Login</button>
  </form>
{% endblock %}
```

---

## templates/day.html

```html
{% extends "layout.html" %}
{% block body %}
  <a href="/">← Back to challenges</a>
  <h2>{{ day|capitalize }}</h2>
  <div class="challenge">{{ content|safe }}</div>

  {% if user %}
    {% if is_solved %}
      <p class="solved">You already solved this! ⭐</p>
    {% else %}
      <form method="post" action="/submit/{{ day }}">
        <label>Enter your answer:</label>
        <input name="answer" required />
        <button type="submit">Submit</button>
      </form>
    {% endif %}
  {% else %}
    <p><a href="/login">Login</a> to submit an answer and track progress.</p>
  {% endif %}
{% endblock %}
```

---

## static/style.css

```css
body { font-family: system-ui, -apple-system, Segoe UI, Roboto, "Helvetica Neue", Arial; max-width: 900px; margin: 0 auto; padding: 1rem; background: #f6f5ff; color: #1f1f2e; }
header { display:flex; justify-content:space-between; align-items:center; }
header h1 a { text-decoration:none; color:inherit }
.days { list-style:none; padding:0 }
.days li { margin: 0.4rem 0 }
.challenge { background: white; padding:1rem; border-radius:8px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }
.flashes { list-style:none; padding:0 }
.flashes li { background: #fff3cd; padding:0.5rem; border-radius:6px; margin-bottom:0.5rem }
.solved { color: green }
.star { margin-left:0.6rem }
footer { margin-top:2rem; color: #6b6b7a }
```

---

## data/answers.json

This file contains the correct answers for each day (strings or numbers). Replace values if you want different answers.

```json
{
  "day01": "5",
  "day02": "3",
  "day03": "4",
  "day04": "2",
  "day05": "7",
  "day06": "6",
  "day07": "9",
  "day08": "8",
  "day09": "10",
  "day10": "12",
  "day11": "11",
  "day12": "14",
  "day13": "13",
  "day14": "15",
  "day15": "16",
  "day16": "17",
  "day17": "18",
  "day18": "19",
  "day19": "20",
  "day20": "21",
  "day21": "22",
  "day22": "23",
  "day23": "24",
  "day24": "25",
  "day25": "26",
  "day26": "27",
  "day27": "28",
  "day28": "29",
  "day29": "30",
  "day30": "31"
}
```

---

## data/progress.json

Initial file (auto-created). Tracks each user's solved days.

```json
{
  "users": {}
}
```

---

## challenges/day01.md .. day30.md

Below are concise beginner-friendly challenge files (fantasy-themed). Each file contains the story, input format, and goal. The expected correct answer values are in `data/answers.json` above (you can change them).


### day01.md
```markdown
# Day 01 — The Wizard's Counting Spell 🪄
You meet a friendly wizard who gives you a short list of numbers. Sum them to prove your arithmetic skills.

**Input:** A list of integers, one per line.
**Goal:** Output the sum of the numbers.

**Example Input:**
```
3
-2
5
-1
```
**Expected Output:**
```
5
```
```

### day02.md
```markdown
# Day 02 — Even Goblins
A goblin merchant asks: how many potions have an even quantity?

**Input:** A list of integers, one per line.
**Goal:** Output the count of even numbers.

**Example Input:**
```
1
2
3
4
```
**Expected Output:**
```
2
```
```

### day03.md
```markdown
# Day 03 — The Door of Vowels
The mansion door accepts a code: count vowels in a single word.

**Input:** A single word (letters only).
**Goal:** Output the number of vowels (a,e,i,o,u).

**Example Input:**
```
magic
```
**Expected Output:**
```
2
```
```

### day04.md
```markdown
# Day 04 — Leap Year Riddle
The village bard asks if a given year is a leap year.

**Input:** A single integer (year).
**Goal:** Output 1 if leap year, else 0. (Simple rule: divisible by 4.)

**Example Input:**
```
2024
```
**Expected Output:**
```
1
```
```

### day05.md
```markdown
# Day 05 — Highest Treasure
Find the largest number in a list of treasure values.

**Input:** Integers, one per line.
**Goal:** Output the maximum value.

**Example Input:**
```
3
9
2
```
**Expected Output:**
```
9
```
```

### day06.md
```markdown
# Day 06 — Average of the Mob
A crowd counts their coins. Compute the integer average (floor).

**Input:** Integers, one per line.
**Goal:** Output the floor of the average.

**Example Input:**
```
3
4
5
```
**Expected Output:**
```
4
```
```

### day07.md
```markdown
# Day 07 — First Duplicate
Find the first number that appears twice (reading top to bottom). If none, output -1.

**Input:** Integers, one per line.
**Goal:** Output the first duplicated number or -1.

**Example Input:**
```
2
5
3
2
```
**Expected Output:**
```
2
```
```

### day08.md
```markdown
# Day 08 — Reverse the Spell
Reverse the letters of a given string.

**Input:** A single line string.
**Goal:** Output the reversed string.

**Example Input:**
```
hello
```
**Expected Output:**
```
olleh
```
```

### day09.md
```markdown
# Day 09 — Sum of Positives
Sum only the positive numbers from a list.

**Input:** Integers, one per line.
**Goal:** Output the sum of positive numbers.

**Example Input:**
```
-1
4
-2
3
```
**Expected Output:**
```
7
```
```

### day10.md
```markdown
# Day 10 — Count Words
Count how many words are on a single line (words separated by spaces).

**Input:** One line of text.
**Goal:** Output the number of words.

**Example Input:**
```
a brave knight
```
**Expected Output:**
```
3
```
```

### day11.md
```markdown
# Day 11 — Odd Sum
Sum only the odd numbers from a list.

**Input:** Integers, one per line.
**Goal:** Output the sum of odd numbers.
```

### day12.md
```markdown
# Day 12 — Multiply Gems
Multiply all numbers in a short list (product).

**Input:** Integers, one per line.
**Goal:** Output the product.
```

### day13.md
```markdown
# Day 13 — Smallest Distance
Given two integers a and b, output |a-b| (absolute difference).

**Input:** Two integers on one line separated by space.
**Goal:** Output the absolute difference.
```

### day14.md
```markdown
# Day 14 — Palindrome Check
Check if a word is a palindrome. Output 1 if yes, else 0.

**Input:** One word.
**Goal:** 1 or 0.
```

### day15.md
```markdown
# Day 15 — Count Letters
Count how many times a specific letter appears in a word.

**Input:** Two tokens: word and single character (space-separated).
**Goal:** Output the count.
```

### day16.md
```markdown
# Day 16 — Sum Until Zero
Read numbers until a 0 appears (0 not included). Output the sum.

**Input:** Integers, ends with 0.
**Goal:** Sum of numbers before 0.
```

### day17.md
```markdown
# Day 17 — Replace Vowels
Replace all vowels in a string with '*'. Output the new string.
```

### day18.md
```markdown
# Day 18 — Even Odd Sort
Given a list of integers, output them sorted with evens first (ascending), then odds (ascending). Output as space-separated.
```

### day19.md
```markdown
# Day 19 — Simple Fibonacci
Output the Nth Fibonacci number (0-based, fib(0)=0, fib(1)=1). Assume N small (<20).

**Input:** Single integer N.
```

### day20.md
```markdown
# Day 20 — Count Unique
Count how many unique numbers are in the list.
```

### day21.md
```markdown
# Day 21 — Reverse Words
Reverse the order of words in a line.
```

### day22.md
```markdown
# Day 22 — Smallest K
Given K then N numbers, output the smallest K numbers sorted ascending.

**Input:** First number K, then numbers separated by spaces.
```

### day23.md
```markdown
# Day 23 — Sum of Digits
Given a number, output the sum of its digits.
```

### day24.md
```markdown
# Day 24 — Caesar Shift
Shift letters in a lowercase word by 1 (z -> a). Output new word.
```

### day25.md
```markdown
# Day 25 — Count Lines
Count how many non-empty lines are in input.
```

### day26.md
```markdown
# Day 26 — Max Consecutive
Find the length of the longest run of equal numbers.
```

### day27.md
```markdown
# Day 27 — Simple Prime
Check if a number is prime (2 or greater): output 1 if prime else 0.
```

### day28.md
```markdown
# Day 28 — Remove Duplicates
Given numbers, output them in original order but with duplicates removed (first occurrence kept). Space-separated.
```

### day29.md
```markdown
# Day 29 — Triangle Check
Given three side lengths, output 1 if they can form a triangle, else 0.
```

### day30.md
```markdown
# Day 30 — Final Treasure
Add the first and last numbers of a list and output the sum.
```
```

---

## requirements.txt

```
flask
markdown
```

---

## README.md

```
# CodeQuest — Fantasy Adventure

Run locally:

1. Create a Python venv (optional): `python -m venv venv` and `source venv/bin/activate`
2. Install requirements: `pip install -r requirements.txt`
3. Run: `python app.py`
4. Open a browser on another device in your home network and go to `http://<your-pc-ip>:5000`.

Login with a simple username (no password) and submit answers to track progress per user.

To change correct answers, edit `data/answers.json`.

Enjoy!
```

