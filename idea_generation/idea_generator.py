import openai
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

def generate_ideas(niche):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    response = openai.Completion.create(
      engine="gpt-3.5-turbo-instruct", 
      prompt=f"Generate video ideas about {niche}",
      max_tokens=120
    )

    return response.choices[0].text.strip().split('\n')

def choose_best_idea(ideas):
    # Criterio simple: elegir la idea más larga
    return max(ideas, key=len)

def generate_and_choose_idea(niche):
    # ... mismo código para generar ideas
    ideas = generate_ideas(niche)
    return choose_best_idea(ideas)


