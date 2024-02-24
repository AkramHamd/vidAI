import openai
import os
from dotenv import load_dotenv
from idea_generator import choose_best_idea


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

# ... mismo código en title_generator.py

"""
# Generar título para la mejor idea
best_title = generate_title(choose_best_idea)
print(best_title)

"""
