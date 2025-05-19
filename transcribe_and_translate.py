import whisper
import os
import json

model = whisper.load_model("base")
video_path = "public/sample-video.mp4"
result = model.transcribe(video_path, language='es')

# Résultat brut pour debug
print("Transcription brute :")
for seg in result["segments"]:
    print(f"[{seg['start']:.2f} - {seg['end']:.2f}] {seg['text']}")

# Sauvegarde segments pour sous-titres dynamiques
segments = [
    {
        "start": seg["start"],
        "end": seg["end"],
        "text": seg["text"].strip()
    }
    for seg in result["segments"]
]

with open("public/transcription_segments.json", "w", encoding="utf-8") as f:
    json.dump(segments, f, ensure_ascii=False, indent=2)

print("✅ Transcription segments sauvegardés dans public/transcription_segments.json")
