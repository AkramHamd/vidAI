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
        font_size=24,
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

def add_subtitles(
    videofilename,
    outputfilename,
    model_size="base",
    MaxChars=10,
    MaxDuration=1.5,
    MaxGap=0.5,
    font="recursos\Heavitas.ttf",
    subtitle_position="bottom",
    font_size=24,
    font_color="white",
    stroke_color="black",
    stroke_width=1
):
    # Convertir video a audio para transcripción
    audiofilename = videofilename.replace(".mp4", '.mp3')
    input_stream = ffmpeg.input(videofilename)
    audio = input_stream.audio
    output_stream = ffmpeg.output(audio, audiofilename)
    ffmpeg.overwrite_output(output_stream).run()

    model = WhisperModel(model_size)
    segments, info = model.transcribe(audiofilename, word_timestamps=True)
    segments = list(segments)

    wordlevel_info = []
    for segment in segments:
        for word in segment.words:
            wordlevel_info.append({'word': word.word, 'start': word.start, 'end': word.end})

    linelevel_subtitles = split_text_into_lines(data=wordlevel_info, MaxChars=MaxChars, MaxDuration=MaxDuration, MaxGap=MaxGap)

    input_video = VideoFileClip(videofilename)
    video_duration = input_video.duration

    frame_size = input_video.size

    all_linelevel_splits = []
    for line in linelevel_subtitles:
        out_clips, positions = create_caption(
            textJSON=line, framesize=frame_size, font=font, 
            font_size=font_size, color=font_color, 
            stroke_color=stroke_color, stroke_width=stroke_width
        )
    
        clip_to_overlay = CompositeVideoClip(out_clips)
        if subtitle_position == "bottom":
            clip_to_overlay = clip_to_overlay.set_position(("center", "bottom"))
        elif subtitle_position == "top":
            clip_to_overlay = clip_to_overlay.set_position(("center", "top"))
        else:
            clip_to_overlay = clip_to_overlay.set_position("center")

        all_linelevel_splits.append(clip_to_overlay)

    
    # Crear CompositeVideoClip con subtítulos
    final_video_with_subtitles = CompositeVideoClip([input_video] + all_linelevel_splits)
    
    # Establecer la duración del CompositeVideoClip
    final_video_with_subtitles = final_video_with_subtitles.set_duration(video_duration)

    final_video_with_subtitles.write_videofile(outputfilename, codec="libx264")

    if os.path.exists(audiofilename):
        os.remove(audiofilename)

    return outputfilename  # Retornar el nombre del archivo generado

#add_subtitles()