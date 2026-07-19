from flask import request, jsonify
from flask_login import login_required

from app.ai import ai
from app.services.ai_service import summarize_text


@ai.route("/ai/summarize", methods=["POST"])
@login_required
def summarize():

    data = request.get_json()

    text = data.get("text", "")

    if not text.strip():
        return jsonify({"error": "No text provided"}), 400

    summary = summarize_text(text)

    return jsonify({
        "summary": summary
    })