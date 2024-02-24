#idea_generator.py
import openai
import re
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

def reformulate_idea_to_short_title(idea):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Pedir a ChatGPT que reformule la idea en un título corto y atractivo para YouTube
    prompt = f"Reformulate this video idea into an attractive, intriguing YouTube title under 100 characters: '{idea}'"
    
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=60,  # Limitar la cantidad de tokens para controlar la longitud del título
        temperature=0.7,  # Ajustar según la creatividad deseada
    )
    
    # Tomar la versión acortada como el título final
    short_title = response.choices[0].text.strip()

    # Verificar si aún necesita acortarse y realizar ajustes si es necesario
    if len(short_title) > 100:
        print("Aún después de reformular, el título supera los 100 caracteres. Se realizarán ajustes automáticos.")
        short_title = short_title[:100]  # Asegurar que el título no exceda 100 caracteres

    return short_title

def choose_best_idea(ideas):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Unir las ideas y crear el prompt para ChatGPT
    ideas_text = "\n".join(ideas)
    prompt = f"Here are some video ideas about a specific niche:\n\n{ideas_text}\n\nWhich one do you think is the most intriguing and interesting, and would also fit within a title of 100 characters or less?"

    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=60,
        temperature=0.5,
    )

    selected_idea = response.choices[0].text.strip()

    if len(selected_idea) > 100:
        print("La idea seleccionada supera los 100 caracteres. Solicitando a ChatGPT una versión más corta...")
        selected_idea = reformulate_idea_to_short_title(selected_idea)
        print(f"Idea reformulada a un título adecuado: {selected_idea}")
    else:
        print(f"Idea seleccionada: {selected_idea}")

    return selected_idea

def generate_and_choose_idea(niche):
    # ... mismo código para generar ideas
    ideas = generate_ideas(niche)
    return choose_best_idea(ideas)


