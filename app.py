import json
import random
from flask import Flask, request, jsonify

app = Flask(__name__)

# ─────────────────────────────
# Load questions ONCE (important for performance)
# ─────────────────────────────

with open("data/sfw.json", "r", encoding="utf-8") as f:
    SFW_QUESTIONS = json.load(f)

with open("data/nsfw.json", "r", encoding="utf-8") as f:
    NSFW_QUESTIONS = json.load(f)


# ─────────────────────────────
# Helper: Select DB by mode
# ─────────────────────────────

def get_questions_by_mode(mode):
    if mode == "nsfw":
        return NSFW_QUESTIONS, "nsfw"
    return SFW_QUESTIONS, "sfw"


# ─────────────────────────────
# 1️⃣ Random Question Endpoint
# GET /?mode=sfw | nsfw
# ─────────────────────────────

@app.route("/", methods=["GET"])
def get_random_question():
    mode = request.args.get("mode", "sfw").lower()
    questions, mode = get_questions_by_mode(mode)

    if not questions:
        return jsonify({
            "success": False,
            "error": "No questions available"
        }), 500

    q = random.choice(questions)

    return jsonify({
        "success": True,
        "id": q["id"],
        "a": q["a"],
        "b": q["b"],
        "votesA": q.get("votesA", 0),
        "votesB": q.get("votesB", 0),
        "mode": mode
    })


# ─────────────────────────────
# 2️⃣ Get Question By ID
# GET /question?id=123&mode=sfw
# ─────────────────────────────

@app.route("/question", methods=["GET"])
def get_question_by_id():
    qid = request.args.get("id")
    mode = request.args.get("mode", "sfw").lower()

    if not qid:
        return jsonify({
            "success": False,
            "error": "Missing question id"
        }), 400

    try:
        qid = int(qid)
    except ValueError:
        return jsonify({
            "success": False,
            "error": "Invalid question id"
        }), 400

    questions, mode = get_questions_by_mode(mode)

    question = next((q for q in questions if q["id"] == qid), None)

    if not question:
        return jsonify({
            "success": False,
            "error": "Question not found"
        }), 404

    return jsonify({
        "success": True,
        "id": question["id"],
        "a": question["a"],
        "b": question["b"],
        "votesA": question.get("votesA", 0),
        "votesB": question.get("votesB", 0),
        "mode": mode
    })


# ─────────────────────────────
# 3️⃣ Both Modes Random Endpoint
# GET /both
# Returns 1 random SFW + 1 random NSFW
# ─────────────────────────────

@app.route("/both", methods=["GET"])
def get_both_random():

    if not SFW_QUESTIONS or not NSFW_QUESTIONS:
        return jsonify({
            "success": False,
            "error": "Questions not available"
        }), 500

    sfw_q = random.choice(SFW_QUESTIONS)
    nsfw_q = random.choice(NSFW_QUESTIONS)

    return jsonify({
        "success": True,
        "sfw": {
            "id": sfw_q["id"],
            "a": sfw_q["a"],
            "b": sfw_q["b"],
            "votesA": sfw_q.get("votesA", 0),
            "votesB": sfw_q.get("votesB", 0),
            "mode": "sfw"
        },
        "nsfw": {
            "id": nsfw_q["id"],
            "a": nsfw_q["a"],
            "b": nsfw_q["b"],
            "votesA": nsfw_q.get("votesA", 0),
            "votesB": nsfw_q.get("votesB", 0),
            "mode": "nsfw"
        }
    })


# ─────────────────────────────
# 4️⃣ Health / Stats Endpoint
# GET /health
# ─────────────────────────────

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "success": True,
        "status": "ok",
        "api": "Would You Rather API",
        "version": "1.2",
        "sfw_count": len(SFW_QUESTIONS),
        "nsfw_count": len(NSFW_QUESTIONS),
        "total_questions": len(SFW_QUESTIONS) + len(NSFW_QUESTIONS)
    })


# ─────────────────────────────
# Run (for local testing)
# ─────────────────────────────

if __name__ == "__main__":
    app.run(debug=True)