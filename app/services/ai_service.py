from google import genai
from flask import current_app

def summarize_text(text):
    client = genai.Client(
        api_key=current_app.config["GOOGLE_API_KEY"]
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
        Summarize the following notes into short bullet points.

        Notes:
        {text}
        """
    )

    return response.text