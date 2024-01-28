import os
import ffmpeg
from faster_whisper import WhisperModel
from moviepy.editor import TextClip, CompositeVideoClip, VideoFileClip, ColorClip

def split_text_into_lines(
        data, 
        MaxChars = 10, 
        MaxDuration = 1.5, 
        MaxGap = 0.5 
    ):

    subtitles = []
    line = []
    line_duration = 0

    for idx,word_data in enumerate(data):
        start = word_data["start"]
        end = word_data["end"]

        line.append(word_data)
        line_duration += end - start

        temp = " ".join(item["word"] for item in line)

        new_line_chars = len(temp)

        duration_exceeded = line_duration > MaxDuration
        chars_exceeded = new_line_chars > MaxChars
        if idx>0:
          gap = word_data['start'] - data[idx-1]['end']
          maxgap_exceeded = gap > MaxGap
        else:
          maxgap_exceeded = False

        if duration_exceeded or chars_exceeded or maxgap_exceeded:
            if line:
                subtitle_line = {
                    "word": " ".join(item["word"] for item in line),
                    "start": line[0]["start"],
                    "end": line[-1]["end"],
                    "textcontents": line
                }
                subtitles.append(subtitle_line)
                line = []
                line_duration = 0

    if line:
        subtitle_line = {
            "word": " ".join(item["word"] for item in line),
            "start": line[0]["start"],
            "end": line[-1]["end"],
            "textcontents": line
        }
        subtitles.append(subtitle_line)

    return subtitles

def create_caption(
        textJSON, 
        framesize,
        font = "Heavitas",
        font_size=46,
        color='white', 
        highlight_color='yellow',
        stroke_color='black',
        stroke_width=1.5
    ):

    full_duration = textJSON['end']-textJSON['start']

    word_clips = []
    xy_textclips_positions =[]

    x_pos = 0
    y_pos = 0
    line_width = 0
    frame_width = framesize[0]
    frame_height = framesize[1]

    x_buffer = frame_width*1/10

    max_line_width = frame_width - 2 * (x_buffer)

    fontsize = int(frame_height * 0.09)

    space_width = ""
    space_height = ""

    for index,wordJSON in enumerate(textJSON['textcontents']):
      duration = wordJSON['end']-wordJSON['start']
      word_clip = TextClip(wordJSON['word'], font=font, fontsize=font_size, 
                     color=color, stroke_color=stroke_color, 
                     stroke_width=stroke_width, bg_color='none')
      word_clip_space = TextClip(" ", font = font,fontsize=fontsize, color=color, bg_color='none').set_start(textJSON['start']).set_duration(full_duration)

      word_width, word_height = word_clip.size
      space_width, space_height = word_clip_space.size
      if line_width + word_width+ space_width <= max_line_width:
            
            xy_textclips_positions.append({
                "x_pos":x_pos,
                "y_pos": y_pos,
                "width" : word_width,
                "height" : word_height,
                "word": wordJSON['word'],
                "start": wordJSON['start'],
                "end": wordJSON['end'],
                "duration": duration
            })

            word_clip = word_clip.set_position((x_pos, y_pos))
            word_clip_space = word_clip_space.set_position((x_pos+ word_width, y_pos))

            x_pos = x_pos + word_width+ space_width
            line_width = line_width+ word_width + space_width
      else:
            x_pos = 0
            y_pos = y_pos+ word_height+10
            line_width = word_width + space_width

            xy_textclips_positions.append({
                "x_pos":x_pos,
                "y_pos": y_pos,
                "width" : word_width,
                "height" : word_height,
                "word": wordJSON['word'],
                "start": wordJSON['start'],
                "end": wordJSON['end'],
                "duration": duration
            })

            word_clip = word_clip.set_position((x_pos, y_pos))
            word_clip_space = word_clip_space.set_position((x_pos+ word_width , y_pos))
            x_pos = word_width + space_width

        


      word_clips.append(word_clip)
      word_clips.append(word_clip_space)


    for highlight_word in xy_textclips_positions:

      word_clip_highlight = TextClip(highlight_word['word'], font = font,fontsize=fontsize, color=highlight_color,stroke_color=stroke_color, bg_color='none',stroke_width=stroke_width).set_start(highlight_word['start']).set_duration(highlight_word['duration'])
      word_clip_highlight = word_clip_highlight.set_position((highlight_word['x_pos'], highlight_word['y_pos']))
      word_clips.append(word_clip_highlight)

    return word_clips,xy_textclips_positions



def add_subtitles(videofilename, outputfilename, model_size="base", MaxChars=10, MaxDuration=1.5, MaxGap=0.5, font="recursos/Heavitas.ttf", subtitle_position="bottom", font_size=46, font_color="white", stroke_color="black", stroke_width=1):
    # Convertir video a audio para transcripción
    audiofilename = videofilename.replace(".mp4", '.mp3')
    ffmpeg.input(videofilename).audio.output(audiofilename).overwrite_output().run()

    model = WhisperModel(model_size)
    segments_gen, info = model.transcribe(audiofilename, word_timestamps=True)
    segments = list(segments_gen)  # Convierte el generador a una lista

    input_video = VideoFileClip(videofilename)
    all_subtitles = []

    for segment in segments:  # Iterar a través de todos los segmentos
        segment_subtitles = []  # Subtítulos para el segmento actual
        last_subtitle_end = 0  # Inicializar el final del último subtítulo en el segmento
        for word in segment.words:
            print(f"Word: {word.word}, Start: {word.start}, End: {word.end}")
            subtitle = TextClip(word.word, font=font, fontsize=font_size, color=font_color, stroke_color=stroke_color, stroke_width=stroke_width, bg_color='none')
            subtitle = subtitle.set_position(("center", "center")).set_start(last_subtitle_end).set_end(word.end)
            segment_subtitles.append(subtitle)  # Agregar el subtítulo al segmento actual
            last_subtitle_end = word.end  # Actualizar el final del último subtítulo en el segmento
        
        # Crear un video compuesto para el segmento actual
        segment_duration = last_subtitle_end  # Duración del segmento
        segment_video = CompositeVideoClip([input_video] + segment_subtitles, size=input_video.size).set_duration(segment_duration)
        all_subtitles.append(segment_video)  # Agregar el video del segmento a la lista de subtítulos finales

    final_video_with_subtitles = CompositeVideoClip(all_subtitles, size=input_video.size).set_duration(input_video.duration)
    final_video_with_subtitles.write_videofile(outputfilename, codec="libx264")

    if os.path.exists(audiofilename):
        os.remove(audiofilename)

    return outputfilename






temp_video_path = "temp_video.mp4"
output_path = "final_video_sub.mp4"

# Añadir subtítulos al video
add_subtitles(videofilename=temp_video_path, outputfilename=output_path)

# Cargar el video para obtener su duración
video_clip = VideoFileClip(temp_video_path)
print(f"Video duration: {video_clip.duration} seconds")

# No olvides cerrar el clip para liberar recursos
video_clip.close()