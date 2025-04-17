import os
import cv2
import pandas as pd
from utils import check_blur, get_resolution
import matplotlib.pyplot as plt
IMAGE_DIR = "images/"
BLUR_THRESHOLD = 100.0
MIN_WIDTH, MIN_HEIGHT = 640, 480

results = []

for filename in os.listdir(IMAGE_DIR):
    if filename.lower().endswith((".jpg", ".png", ".jpeg")):
        image_path = os.path.join(IMAGE_DIR, filename)
        image = cv2.imread(image_path)

        blur_score = check_blur(image)
        width, height = get_resolution(image)

        status = "PASS"
        if blur_score < BLUR_THRESHOLD or width < MIN_WIDTH or height < MIN_HEIGHT:
            status = "FAIL"

        results.append({
            "filename": filename,
            "blur_score": blur_score,
            "resolution": f"{width}x{height}",
            "status": status
        })

df = pd.DataFrame(results)
df.to_csv("outputs/quality_report.csv", index=False)


alerts = df[df["status"] == "FAIL"]
if not alerts.empty:
    alerts.to_csv("logs/alert_report.csv", index=False)
    print("⚠️ Alert: Some images failed quality checks!")
with open("outputs/alerts.txt", "w") as f:
        for _, row in alerts.iterrows():
            f.write(f"[WARNING] {row['filename']} is too blurry: Score = {row['blur_score']}\n")

#graph visul
plt.hist(df['blur_score'], bins=20)
plt.title('Blur Score Distribution')
plt.xlabel('Blur Score')
plt.ylabel('Image Count')
plt.savefig("outputs/blur_distribution.png")
