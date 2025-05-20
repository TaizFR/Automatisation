import cv2
import pytesseract
import numpy as np
import json
import os
import subprocess

input_video_path = "public/sample-video.mp4"
output_video_path = "public/sample-video-blurred.mp4"
langs = ['spa', 'eng']

cap = cv2.VideoCapture(input_video_path)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

num_samples = 80
sampled_indices = [int(i * frame_count / num_samples) for i in range(num_samples)]

heatmap = np.zeros((height, width), dtype=np.float32)

for frame_idx in sampled_indices:
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
    ret, frame = cap.read()
    if not ret:
        continue
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    for lang in langs:
        results = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT, lang=lang)
        for i in range(len(results["text"])):
            text = results["text"][i]
            try:
                conf = float(results["conf"][i])
            except:
                conf = 0
            w = results["width"][i]
            h = results["height"][i]
            if conf > 30 and text.strip() != "" and w > 20:
                x = results["left"][i]
                y = results["top"][i]
                if y > height * 0.6:
                    heatmap[y:y+h, x:x+w] += 1

cap.release()

max_heat = heatmap.max()
if max_heat == 0:
    x, y, w, h = int(width*0.2), int(height*0.75), int(width*0.6), int(height*0.1)
else:
    thresh = max(2, max_heat * 0.4)
    mask = (heatmap >= thresh).astype(np.uint8)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    boxes = [cv2.boundingRect(c) for c in contours if cv2.contourArea(c) > 200]

    if boxes:
        min_x = min([box[0] for box in boxes])
        min_y = min([box[1] for box in boxes])
        max_x = max([box[0] + box[2] for box in boxes])
        max_y = max([box[1] + box[3] for box in boxes])

        # Marges à ajuster à ta convenance
        extra_left = 215     # marge de sécurité à gauche
        extra_right = 115    # marge de sécurité à droite
        top_margin = 12
        bottom_margin = 6

        x = max(min_x - extra_left, 0)
        y = max(min_y - top_margin, 0)
        w = min((max_x - min_x) + extra_left + extra_right, width - x)
        h = min((max_y - min_y) + top_margin + bottom_margin, height - y)
    else:
        x, y, w, h = int(width*0.2), int(height*0.75), int(width*0.6), int(height*0.1)

with open("public/blur_box.json", "w") as f:
    json.dump({"x": int(x), "y": int(y), "width": int(w), "height": int(h)}, f)

cap = cv2.VideoCapture(input_video_path)
ret, frame = cap.read()
if ret:
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imwrite("public/debug_box.jpg", frame)
cap.release()

cap = cv2.VideoCapture(input_video_path)
fps = cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
while True:
    ret, frame = cap.read()
    if not ret:
        break
    sub_img = frame[y:y+h, x:x+w]
    blurred = cv2.GaussianBlur(sub_img, (51, 51), 75)
    frame[y:y+h, x:x+w] = blurred
    out.write(frame)
cap.release()
out.release()

print(f"✅ Rectangle auto détecté : x={x} y={y} w={w} h={h}")

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


