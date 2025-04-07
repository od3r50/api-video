from flask import Flask, request, jsonify, send_file
from moviepy.editor import *
import json
from uuid import uuid4
from config import VIDEO_DIR
from services import file_utils

app = Flask(__name__)

def load_template(template_id, modifications):
    path = f"templates/{template_id}.json"
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

@app.route("/render", methods=["POST"])
def render_video():
    body = request.json
    template_id = body.get("template_id")
    modifications = body.get("modifications", {})

    try:
        data = load_template(template_id, modifications)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    clips = []
    audio_clips = []
    temp_dirs = []

    try:
        for el in data["elements"]:
            tipo = el["type"]
            time = el["time"]
            duration = el["duration"]

            if tipo == "video":
                src = el["source"]
                video_path, temp_dir = file_utils.download_file(src)
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
                audio_path, temp_dir = file_utils.download_file(src)
                temp_dirs.append(temp_dirs)
                audio = AudioFileClip(audio_path).subclip(0, duration).set_start(time)
                audio_clips.append(audio)

        final = CompositeVideoClip(clips, size=(data["width"], data["height"]))

        if audio_clips:
            combined_audio = CompositeAudioClip(audio_clips)
            final = final.set_audio(combined_audio)

        output_path = os.path.join(VIDEO_DIR, f"{uuid4().hex}.mp4")
        final.write_videofile(output_path, fps=24)

        return send_file(output_path, as_attachment=True)
    
    finally:
        for td in temp_dirs:
            file_utils.clean_temp_files(td)

# @app.route("/download", methods=["GET"])
# def download():
#     path = request.args.get("path")
#     if not os.path.exists(path):
#         return jsonify({"error": "Arquivo não encontrado"}), 404
#     return send_file(path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
