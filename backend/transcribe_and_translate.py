import whisper
import os
from deep_translator import GoogleTranslator
import json

print("🎙️ Début transcription segmentée...")

model = whisper.load_model("base")
video_path = os.path.join("public", "sample-video.mp4")
result = model.transcribe(video_path)

segments = result["segments"]

# Traduction segment par segment
translated_segments = []

for seg in segments:
    original_text = seg["text"].strip()
    translated_text = GoogleTranslator(source='auto', target='hi').translate(original_text)
    translated_segments.append({
        "start": seg["start"],
        "end": seg["end"],
        "original": original_text,
        "translated": translated_text
    })

# Sauvegarde en JSON
with open("public/translated_segments.json", "w", encoding="utf-8") as f:
    json.dump(translated_segments, f, ensure_ascii=False, indent=2)

print("✅ Fichier JSON prêt : public/translated_segments.json")
