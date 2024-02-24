from flask import Flask
from idea_generation.title_generator import setup_routes as setup_title_routes
from idea_generation.idea_generator import setup_routes as setup_idea_routes
from image_generation.image_generator import setup_routes as setup_image_routes


app = Flask(__name__)

# Registra las rutas para el generador de ideas
setup_idea_routes(app)
setup_title_routes(app)
setup_image_routes(app)

@app.route('/')
def home():
    return "Bienvenido a la API de Video AI!"

if __name__ == '__main__':
    app.run(debug=True)
