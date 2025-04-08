from flask import Blueprint, request, jsonify, send_file
from moviepy.editor import *
import json
from services.file_utils import clean_temp_files
from services.video import process_elements


bp = Blueprint("render", __name__)

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

@bp.route("/render", methods=["POST"])
def render_video():
    body = request.json
    temp_dirs = []

    try:
        data = load_template(body["template_id"], body.get("modifications", {}))
        video_path, temp_dirs = process_elements(data)
        return send_file(video_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
    finally:
        for td in temp_dirs:
            clean_temp_files(td)