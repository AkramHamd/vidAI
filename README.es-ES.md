

# 🎥 Video AI Python Project

## Descripción

Este proyecto es una herramienta de automatización para la creación y edición de videos utilizando Python. Integra tecnologías como MoviePy, FFmpeg y Whisper para el procesamiento de video, audio y generación de subtítulos.

## Características

  - Redimensionamiento de imágenes: Ajusta imágenes al tamaño de video deseado.
  - Efectos visuales: Incluye efectos como 'camera shake' para dinamizar el video.
  - Subtítulos automáticos: Utiliza Whisper para transcribir audio y generar subtítulos sincronizados.
  - Overlay de partículas: Añade un efecto de partículas sobre el video.

## Requisitos

  - Python 3.8 o superior
  - MoviePy
  - FFmpeg
  - Whisper
  - ImageMagick (para Windows)

## Instalación

Clona el repositorio:

  git clone https://github.com/AkramHamd/vidAI.git

## Instala las dependencias:

  pip install -r requirements.txt

## Uso

  - Coloca tus imágenes y archivos de audio en las carpetas correspondientes.
  - Ejecuta el script principal:

  python video_creator.py

  - Los videos se guardarán en la carpeta de salida especificada.

## Estructura del Proyecto

  video-ai-python/
  ├── .temp/
  │   ├── temp_resized_images/ (Directorio para imágenes redimensionadas)
  │   ├── temp_video.mp4 (Video temporal sin subtítulos)
  │   └── final_video_sub.mp4 (Video final con subtítulos)
  ├── downloaded_images/ (Directorio para imágenes descargadas)
  ├── idea_generation/
  │   ├── __init__.py
  │   ├── idea_generator.py
  │   └── title_generator.py
  ├── image_generation/
  │   ├── __init__.py
  │   └── image_generator.py
  ├── recursos/
  │   ├── Heavitas.ttf (y otras fuentes o recursos)
  │   └── ...
  ├── script_generation/
  │   ├── __init__.py
  │   └── script_generator.py
  ├── subtitles/
  │   ├── __init__.py
  │   └── subtitle_generator.py
  ├── thumbnail_generation/
  │   ├── __init__.py
  │   └── thumbnail_creator.py
  ├── tts_generation/
  │   ├── __init__.py
  │   └── tts_generator.py
  ├── utils/
  │   ├── __init__.py
  │   └── utils.py
  ├── video_creation/
  │   ├── __init__.py
  │   └── video_creator.py
  ├── youtube_upload/
  │   ├── __init__.py
  │   └── ...
  ├── videos/ (Directorio para videos generados)
  └── venv/ (Entorno virtual de Python)


## Contribuciones

Las contribuciones son bienvenidas. Por favor, envía un pull request o abre un issue para sugerir cambios o mejoras.
Licencia

Este proyecto está bajo la licencia MIT.

## Tareas Pendientes

- [x] Corregir la vibración de la cámara (Fix camera shake).
- [ ] Corregir la función de zoom (Fix zoom).
- [ ] Añadir logger
- [x] Añadir subtítulos dinámicos
- [ ] Desarrollar la función principal (Elaborate main).
- [ ] Agregar transiciones (Add transitions).
- [ ] Agregar generador de miniaturas
- [ ] Corregir overlays
- [x] Añadir subida automática a YouTube
