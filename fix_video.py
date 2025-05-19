import os
import subprocess

# Nom du fichier d'entrée et de sortie
input_file = "public/sample-video-blurred.mp4"
output_file = "public/sample-video-blurred-fixed.mp4"

def fix_video(input_path, output_path):
    # Utilise FFmpeg pour réencoder la vidéo sans toucher à la qualité
    cmd = [
        "ffmpeg",
        "-y",  # overwrite sans demander
        "-i", input_path,
        "-c:v", "libx264",  # H.264 pour la vidéo
        "-c:a", "aac",      # AAC pour l'audio (optionnel)
        "-movflags", "+faststart",  # permet une lecture directe en streaming/web
        output_path
    ]
    print("Réencodage en cours...")
    subprocess.run(cmd, check=True)
    print("✅ Réencodage terminé :", output_path)

if __name__ == "__main__":
    if not os.path.exists(input_file):
        print(f"❌ Fichier d'entrée introuvable : {input_file}")
    else:
        fix_video(input_file, output_file)
