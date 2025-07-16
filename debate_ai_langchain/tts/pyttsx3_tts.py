import pyttsx3

def generate_tts(text, filename, voice_index=0):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    # Choose voice by index (0 or 1)
    if voice_index < len(voices):
        selected_voice = voices[voice_index]
    else:
        selected_voice = voices[0]  # fallback

    engine.setProperty('voice', selected_voice.id)
    engine.setProperty('rate', 160)
    engine.setProperty('volume', 0.9)

    print(f"[🗣️] Using voice: {selected_voice.name}")
    engine.save_to_file(text, f'static/{filename}')
    engine.runAndWait()