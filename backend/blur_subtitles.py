import cv2
import pytesseract

input_video_path = "public/sample-video.mp4"
output_video_path = "public/sample-video-blurred.mp4"
langs = ['spa', 'eng']

cap = cv2.VideoCapture(input_video_path)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

num_samples = 18  # Plus tu mets d'échantillons, mieux tu couvres les cas bizarres
sampled_indices = [int(i * frame_count / num_samples) for i in range(num_samples)]

all_lefts = []
all_rights = []
all_tops = []
all_bottoms = []

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
            conf_str = results["conf"][i]
            try:
                conf = float(conf_str)
            except:
                conf = 0
            w = results["width"][i]
            h = results["height"][i]
            if conf > 30 and text.strip() != "" and w > 25:
                x = results["left"][i]
                y = results["top"][i]
                if y > height * 0.5:
                    all_lefts.append(x)
                    all_rights.append(x + w)
                    all_tops.append(y)
                    all_bottoms.append(y + h)
cap.release()

# Marge de sécurité pour ne JAMAIS couper le texte
padding_x = 45
padding_y = 15

if all_lefts and all_rights and all_tops and all_bottoms:
    x1 = max(0, min(all_lefts) - padding_x)
    x2 = min(width, max(all_rights) + padding_x)
    y1 = max(0, min(all_tops) - padding_y)
    y2 = min(height, max(all_bottoms) + padding_y)
else:
    y1 = int(height * 0.75)
    y2 = int(height * 0.82)
    x1 = int(width * 0.2)
    x2 = int(width * 0.8)

print(f"\n➡️ Rectangle flou ABSOLU : x1={x1}, y1={y1}, x2={x2}, y2={y2} ({x2-x1}x{y2-y1}px)\n")

cap = cv2.VideoCapture(input_video_path)
fps = cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

while True:
    ret, frame = cap.read()
    if not ret:
        break
    sub_img = frame[y1:y2, x1:x2]
    blurred = cv2.GaussianBlur(sub_img, (31, 31), 30)
    frame[y1:y2, x1:x2] = blurred
    out.write(frame)
cap.release()
out.release()
print(f"\n✅ Vidéo exportée : {output_video_path}\n")
