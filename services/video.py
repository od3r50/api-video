from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, CompositeAudioClip, AudioFileClip
from services.file_utils import download_file
from config import VIDEO_DIR
import os
from uuid import uuid4
from threading import Thread

def render_clip_in_thread(clip, audio_clip, output, fps, job_id=None, jobs_dict=None):
    def render():
        try:
            final_clip = clip.set_audio(audio_clip) if audio_clip else clip
            final_clip.write_videofile(output, fps=fps)

            if jobs_dict is not None and job_id:
                jobs_dict[job_id]["status"] = "done"
                jobs_dict[job_id]["path"] = output

        except Exception as e:
            if jobs_dict is not None and job_id:
                jobs_dict[job_id] = {"status": "error", "message": str(e)}

    t = Thread(target=render)
    t.start()

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

def render_worker(data, output_path):
    from services.file_utils import clean_temp_files

    temp_dirs = []
    try:
        _, temp_dirs = process_elements(data)
        print(f"[INFO] Render finalizado: {output_path}")
    except Exception as e:
        print(f"[ERRO] Render falhou: {e}")

    finally:
        for td in temp_dirs:
            clean_temp_files(td)