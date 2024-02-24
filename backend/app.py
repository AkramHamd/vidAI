from flask import Flask, jsonify, request

# Asegúrate de que los nombres de las funciones no entren en conflicto
from idea_generation.idea_generator import *

app = Flask(__name__)

setup_routes(app)

@app.route('/')
def home():
    return "Bienvenido a la API de Video AI!"



if __name__ == '__main__':
    app.run(debug=True)
