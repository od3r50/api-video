from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, CompositeAudioClip, AudioFileClip
from app.services.file_utils import download_file
import os
import json

def load_template(template_id, modifications):
    path = f"app/templates/{template_id}.json"
    if not os.path.exists(path):
        raise FileNotFoundError("Template not found.")

    with open(path, "r") as f:
        template = json.load(f)

    for el in template["elements"]:
        name = el.get("name")
        if not name:
            continue
        for field, value in modifications.items():
            if field.startswith(name + "."):
                prop = field.split(".", 1)[1]
                el[prop] = value
    return template

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
            temp_dirs.append(temp_dir)
            audio = AudioFileClip(audio_path).subclip(0, duration).set_start(time)
            audio_clips.append(audio)

    final_clip = CompositeVideoClip(clips, size=(data["width"], data["height"]))
    combined_audio = CompositeAudioClip(audio_clips) if audio_clips else None

    return final_clip, combined_audio, temp_dirs
