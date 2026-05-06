import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import time

# Settings
FRAME_SKIP_NORMAL = 5
FRAME_SKIP_MOTION = 2
MOTION_THRESHOLD = 500

# Global variables
prev_gray = None
frame_skip = FRAME_SKIP_NORMAL
frame_count = 0

def resize_frame(frame):
    return cv2.resize(frame, (640, 480))

def detect_motion(frame):
    global prev_gray, frame_skip
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    if prev_gray is None:
        prev_gray = gray
        return False
    diff = cv2.absdiff(prev_gray, gray)
    score = np.sum(diff > 25)
    prev_gray = gray
    if score > MOTION_THRESHOLD:
        frame_skip = FRAME_SKIP_MOTION
        return True
    frame_skip = FRAME_SKIP_NORMAL
    return False

def detect_person(frame, detector):
    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    )
    result = detector.detect(mp_image)
    persons = [d for d in result.detections
               if d.categories[0].category_name == "person"
               and d.categories[0].score > 0.5]
    return persons

def process_frame(frame, detector):
    global frame_count
    frame_count += 1
    if frame_count % frame_skip != 0:
        return None
    small = resize_frame(frame)
    motion = detect_motion(small)
    if not motion:
        return None
    persons = detect_person(small, detector)
    if persons:
        confidence = round(persons[0].categories[0].score * 100)
        print(f"ALERT! Person detected - {confidence}% confidence")
        return {"alert": True, "confidence": confidence}
    return None

print("SecurLens Bridge Software Ready!")
print("Version 1.0")
