from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, CompositeAudioClip, AudioFileClip
from services.file_utils import download_file
from config import VIDEO_DIR
import os
from uuid import uuid4

def process_elements(data):
    clips = []
    audio_clips = []
    temp_dirs = []

    for el in data["elements"]:
        tipo = el["type"]
        time = el["time"]
        duration = el["duration"]

        if tipo == "video":
            src = el["source"]
            video_path, temp_dir = download_file(src)
            temp_dirs.append(temp_dir)
            clip = VideoFileClip(video_path).subclip(0, duration).set_start(time)
            clips.append(clip)

        elif tipo == "text":
            txt = TextClip(
                el["text"],
                fontsize=el.get("font_size", 20),
                color='white',
                font="Arial-Bold"
            ).set_position(("center", el["y"])).set_duration(duration).set_start(time)
            clips.append(txt)

        elif tipo == "audio":
            src = el["source"]
            audio_path, temp_dir = download_file(src)
            temp_dirs.append(temp_dirs)
            audio = AudioFileClip(audio_path).subclip(0, duration).set_start(time)
            audio_clips.append(audio)

    final = CompositeVideoClip(clips, size=(data["width"], data["height"]))

    if audio_clips:
        combined_audio = CompositeAudioClip(audio_clips)
        final = final.set_audio(combined_audio)

    output = os.path.join(VIDEO_DIR, f"{uuid4().hex}.mp4")
    final.write_videofile(output, fps=24)

    return output, temp_dirs