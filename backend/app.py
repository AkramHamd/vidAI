from flask import Flask
# Importa la función de configuración de rutas para el generador de títulos
from idea_generation.title_generator import setup_routes as setup_title_routes
# Importa la función de configuración de rutas para el generador de ideas
from idea_generation.idea_generator import setup_routes as setup_idea_routes

app = Flask(__name__)

# Registra las rutas para el generador de ideas
setup_idea_routes(app)
# Registra las rutas para el generador de títulos
setup_title_routes(app)

@app.route('/')
def home():
    return "Bienvenido a la API de Video AI!"

if __name__ == '__main__':
    app.run(debug=True)
