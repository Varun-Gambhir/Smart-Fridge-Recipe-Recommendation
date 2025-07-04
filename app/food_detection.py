import subprocess
import cv2
import os
import re
import json
from collections import Counter
from utils import client

def capture_image(output_path="data/captured.jpg", width=1640, height=1232):
    try:
        subprocess.run([
            "libcamera-still",
            "-o", output_path,
            "--width", str(width),
            "--height", str(height),
            "--nopreview",
            "--timeout", "1"
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        return True
    except Exception as e:
        print(f"Camera error: {e}")
        return False

def detect_food_items(image_path):
    try:
        if not os.path.exists(image_path):
            return []
        
        my_file = client.files.upload(file=image_path)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[my_file, "Detect all of the prominent food ingredients list in the image. The box_2d should be [ymin, xmin, ymax, xmax] normalized to 0-1000. All of the fruits/vegetables must be named. Provide separate bounding boxes for each individual item, even if they are the same type of food."],
        )
        
        json_str = re.search(r'\[\s*{.*?}\s*\]', response.text, re.DOTALL)
        if json_str:
            try:
                return json.loads(json_str.group(0))
            except json.JSONDecodeError:
                pass
        
        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            return []
    except Exception:
        return []

def count_food_items(annotations):
    food_counts = Counter()
    for ann in annotations:
        if "label" in ann:
            label = ann["label"].strip().lower()
            food_counts[label] += 1
    return food_counts

def create_annotated_image(image_path, annotations):
    try:
        image = cv2.imread(image_path)
        if image is None:
            return None
            
        height, width, _ = image.shape
        food_counts = Counter()
        
        for ann in annotations:
            if "box_2d" not in ann or "label" not in ann:
                continue
                
            ymin, xmin, ymax, xmax = ann["box_2d"]
            label = ann["label"].strip().lower()
            food_counts[label] += 1
            count = food_counts[label]
            
            x1 = int((xmin / 1000) * width)
            y1 = int((ymin / 1000) * height)
            x2 = int((xmax / 1000) * width)
            y2 = int((ymax / 1000) * height)
            
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 3)
            display_label = f"{label} ({count})" if food_counts[label] > 1 else label
            text_size = cv2.getTextSize(display_label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
            cv2.rectangle(image, (x1, y1 - text_size[1] - 10), 
                         (x1 + text_size[0], y1), (0, 255, 0), -1)
            cv2.putText(image, display_label, (x1, y1 - 5), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        
        annotated_path = "data/annotated.jpg"
        cv2.imwrite(annotated_path, image)
        return annotated_path
    except Exception:
        return None