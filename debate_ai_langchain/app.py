from flask import Flask, render_template, send_file, request
from flask_socketio import SocketIO
from agents.debater_uk import generate_uk_debate_speech
from agents.debater_asia import generate_asia_debate_speech
from agents.adjudicator import judge_apd_debate, judge_bpd_debate
from tts.pyttsx3_tts import generate_tts
import os
import threading
import traceback
import re

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# 🧹 Cleanup logic to remove only generated output files
def clear_previous_outputs():
    static_dir = "static"
    safe_to_delete = ["for_speaker.wav", "against_speaker.wav", "debate_result.txt"]
    for filename in safe_to_delete:
        file_path = os.path.join(static_dir, filename)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"[🧽] Deleted: {file_path}")
            except Exception as e:
                print(f"[⚠️] Could not delete {file_path}: {e}")

@app.route("/", methods=["GET"])
def index():
    clear_previous_outputs()
    return render_template("index.html")

@app.route("/download_txt")
def download_txt():
    return send_file("static/debate_result.txt", as_attachment=True)

def save_transcript(topic, speech_for, speech_against, judgment):
    os.makedirs("static", exist_ok=True)
    txt_path = os.path.join("static", "debate_result.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(f"Debate Topic: {topic}\n\n")
        f.write("FOR the Motion:\n")
        f.write(speech_for + "\n\n")
        f.write("AGAINST the Motion:\n")
        f.write(speech_against + "\n\n")
        f.write("AI Judgment:\n")
        f.write(judgment + "\n")

@socketio.on("start_debate")
def handle_debate(data):
    format_type = data.get("format")
    topic = data.get("topic")
    context = data.get("context")
    sid = request.sid

    def stream_response(sid):
        try:
            if format_type == "BP":
                speech_for = generate_uk_debate_speech(topic, context, role="for")
                socketio.emit("stream_for", {"text": speech_for}, to=sid)

                speech_against = generate_uk_debate_speech(topic, context, role="against")
                socketio.emit("stream_against", {"text": speech_against}, to=sid)

                judgment = judge_bpd_debate(speech_for, speech_against, topic, context)
            else:
                speech_for = generate_asia_debate_speech(topic, context, role="for")
                socketio.emit("stream_for", {"text": speech_for}, to=sid)

                speech_against = generate_asia_debate_speech(topic, context, role="against")
                socketio.emit("stream_against", {"text": speech_against}, to=sid)

                judgment = judge_apd_debate(speech_for, speech_against, topic, context)

            socketio.emit("stream_judgment", {"judgment": judgment}, to=sid)
            save_transcript(topic, speech_for, speech_against, judgment)

            def clean_text(text):
                """Clean unwanted tags and symbols for TTS."""
                text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
                text = re.sub(r"[-*]", "", text)
                return text.strip()

            speech_for_clean = clean_text(speech_for)
            speech_against_clean = clean_text(speech_against)

            generate_tts(speech_for_clean, "for_speaker.wav", voice_index=0)
            generate_tts(speech_against_clean, "against_speaker.wav", voice_index=1)

            socketio.emit("stream_done", {"txt_link": "/download_txt"}, to=sid)

        except Exception as e:
            print("[❌ ERROR] Debate generation failed:")
            traceback.print_exc()
            socketio.emit("stream_judgment", {"judgment": "❌ An error occurred. Please try again."}, to=sid)
            socketio.emit("stream_done", {}, to=sid)

    threading.Thread(target=stream_response, args=(sid,)).start()

if __name__ == "__main__":
    socketio.run(app, debug=True)
