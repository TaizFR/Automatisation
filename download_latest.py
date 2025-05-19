import subprocess
import os

print("✅ Script lancé.")

output_path = os.path.join("public", "sample-video.mp4")
yt_dlp_exe = os.path.join(os.getcwd(), "yt-dlp.exe")

command = [
    yt_dlp_exe,
    "-f", "mp4",
    "--output", output_path,
    "--playlist-items", "1",
    "--force-overwrites",
    "https://www.youtube.com/@YoSoyZnd/shorts"
]


print("▶️ Commande :", " ".join(command))

result = subprocess.run(command)
if result.returncode == 0:
    print("✅ Téléchargement terminé sans erreur.")
elif result.returncode == 101:
    print("ℹ️ Téléchargement terminé avec code 101 (déjà téléchargé ou interruption prévue).")
else:
    print(f"❌ yt-dlp a retourné une erreur (code {result.returncode})")
