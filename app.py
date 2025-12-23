import json
import random
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load questions ONCE (important for performance)
with open("data/sfw.json", "r", encoding="utf-8") as f:
    SFW_QUESTIONS = json.load(f)

with open("data/nsfw.json", "r", encoding="utf-8") as f:
    NSFW_QUESTIONS = json.load(f)


@app.route("/", methods=["GET"])
def get_question():
    # mode can be: sfw | nsfw
    mode = request.args.get("mode", "sfw").lower()

    if mode == "nsfw":
        questions = NSFW_QUESTIONS
    else:
        questions = SFW_QUESTIONS

    if not questions:
        return jsonify({
            "success": False,
            "error": "No questions available"
        }), 500

    q = random.choice(questions)

    # Return ONLY what bot needs
    return jsonify({
        "success": True,
        "id": q["id"],
        "a": q["a"],
        "b": q["b"],
        "votesA": q.get("votesA", 0),
        "votesB": q.get("votesB", 0),
        "mode": mode
    })
