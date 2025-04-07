from flask import Flask, request, jsonify, send_file
from moviepy.editor import *
import os
import requests
import json
from uuid import uuid4
import tempfile
import shutil

app = Flask(__name__)
VIDEO_DIR = "videos"
os.makedirs(VIDEO_DIR, exist_ok=True)

def baixar_arquivo(url, destino):
    r = requests.get(url, stream=True)
    with open(destino, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

def carregar_template_modificado(template_id, modifications):
    caminho = f"templates/{template_id}.json"
    if not os.path.exists(caminho):
        raise FileNotFoundError("Template não encontrado.")

    with open(caminho, "r") as f:
        template = json.load(f)

    for el in template["elements"]:
        nome = el.get("name")
        if not nome:
            continue
        for campo, valor in modifications.items():
            if campo.startswith(nome + "."):
                prop = campo.split(".", 1)[1]
                el[prop] = valor
    return template

@app.route("/render", methods=["POST"])
def render_video():
    body = request.json
    template_id = body.get("template_id")
    modifications = body.get("modifications", {})

    try:
        data = carregar_template_modificado(template_id, modifications)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
    temp_dir = tempfile.mkdtemp()

    clips = []
    audio_clips = []

    try:
        for el in data["elements"]:
            tipo = el["type"]
            time = el["time"]
            duration = el["duration"]

            if tipo == "video":
                src = el["source"]
                nome_arquivo = os.path.join(temp_dir, f"tmp_{uuid4().hex}.mp4")            
                baixar_arquivo(src, nome_arquivo)
                clip = VideoFileClip(nome_arquivo).subclip(0, duration).set_start(time)
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
                nome_audio = os.path.join(temp_dir, f"tmp_{uuid4().hex}.mp3")
                baixar_arquivo(src, nome_audio)
                audio = AudioFileClip(nome_audio).subclip(0, duration).set_start(time)
                audio_clips.append(audio)

        final = CompositeVideoClip(clips, size=(data["width"], data["height"]))

        if audio_clips:
            combined_audio = CompositeAudioClip(audio_clips)
            final = final.set_audio(combined_audio)

        output_path = os.path.join(VIDEO_DIR, f"{uuid4().hex}.mp4")
        final.write_videofile(output_path, fps=24)

        return send_file(output_path, as_attachment=True)
    
    finally:
        shutil.rmtree(temp_dir)

@app.route("/download", methods=["GET"])
def download():
    path = request.args.get("path")
    if not os.path.exists(path):
        return jsonify({"error": "Arquivo não encontrado"}), 404
    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
