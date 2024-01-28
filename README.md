# vidAI

# 🎥 Video AI Python Project
## Descripción

Este proyecto es una herramienta de automatización para la creación y edición de videos utilizando Python. Integra tecnologías como MoviePy, FFmpeg y Whisper para el procesamiento de video, audio y generación de subtítulos.

## Características

    Redimensionamiento de imágenes: Ajusta imágenes al tamaño de video deseado.
    Efectos visuales: Incluye efectos como 'camera shake' para dinamizar el video.
    Subtítulos automáticos: Utiliza Whisper para transcribir audio y generar subtítulos sincronizados.
    Overlay de partículas: Añade un efecto de partículas sobre el video.

## Requisitos

    Python 3.8 o superior
    MoviePy
    FFmpeg
    Whisper
    ImageMagick (para Windows)

## Instalación

    Clona el repositorio:

    bash

git clone https://github.com/tu-usuario/tu-repo.git

## Instala las dependencias:

    pip install -r requirements.txt

## Uso

    Coloca tus imágenes y archivos de audio en las carpetas correspondientes.
    Ejecuta el script principal:

    python video_creator.py

    Los videos se guardarán en la carpeta de salida especificada.

## Estructura del Proyecto

video-ai-python/
│
├── video_creation/
│   ├── video_creator.py
│   └── subtitle_generator.py
│
├── recursos/
│   ├── particle_overlay.mp4
│   └── fonts/
│       └── Heavitas.ttf
│
├── temp_resized_images/
│
└── videos/
    ├── voiceover.mp3
    └── output/

## Contribuciones

Las contribuciones son bienvenidas. Por favor, envía un pull request o abre un issue para sugerir cambios o mejoras.
Licencia

Este proyecto está bajo la licencia MIT.

## Tareas Pendientes

- [x] Corregir la vibración de la cámara (Fix camera shake).
- [ ] Corregir la función de zoom (Fix zoom).
- [ ] Añadir subtitulos dinamicos
- [ ] Desarrollar la función principal (Elaborate main).
- [ ] Agregar transiciones (Add transitions).
