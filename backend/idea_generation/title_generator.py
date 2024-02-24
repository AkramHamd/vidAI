# idea_generation/title_generator.py
import openai
import os
from flask import request, jsonify
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def generate_title(idea):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=f"Create an engaging and catchy title for a video about: {idea}",
        max_tokens=120
    )

    return response.choices[0].text.strip()

def setup_routes(app):
    @app.route('/generate_title', methods=['POST'])
    def generate_video_title():
        data = request.json
        idea = data.get('idea')
        if not idea:
            return jsonify({"error": "No idea provided"}), 400
        title = generate_title(idea)
        return jsonify({"title": title})
