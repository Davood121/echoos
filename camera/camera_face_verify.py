# camera_face_verify.py - simple capture + compare
import cv2
import numpy as np
import face_recognition
import os
import json

# Config
DB_PATH = '/opt/echoos/data/face_encodings.npz'
# For Windows dev environment, adjust path if needed, or use relative
if os.name == 'nt':
    DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'face_encodings.npz')

def capture_frame():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Could not open camera")
    
    # Warmup
    for _ in range(5):
        cap.read()
        
    ret, frame = cap.read()
    cap.release()
    if not ret:
        raise RuntimeError('Camera read failed')
    return frame

def load_encodings():
    if not os.path.exists(DB_PATH):
        return {}
    try:
        data = np.load(DB_PATH, allow_pickle=True)
        return data['arr_0'].item()
    except Exception as e:
        print(f"Error loading encodings: {e}")
        return {}

def save_encodings(dct):
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    np.savez(DB_PATH, dct)

def enroll_user(name):
    print(f"Enrolling {name}...")
    try:
        frame = capture_frame()
        rgb = frame[:, :, ::-1] # BGR to RGB
        boxes = face_recognition.face_locations(rgb)
        encs = face_recognition.face_encodings(rgb, boxes)
        
        if not encs:
            print("No face found. Please try again.")
            return False
            
        d = load_encodings()
        d[name] = encs[0]
        save_encodings(d)
        print(f"Successfully enrolled {name}")
        return True
    except Exception as e:
        print(f"Enrollment failed: {e}")
        return False

def verify_user(name, tolerance=0.5):
    d = load_encodings()
    if name not in d:
        print(f"User {name} not found.")
        return False
        
    try:
        frame = capture_frame()
        rgb = frame[:, :, ::-1]
        boxes = face_recognition.face_locations(rgb)
        encs = face_recognition.face_encodings(rgb, boxes)
        
        if not encs:
            print("No face detected.")
            return False
            
        # Compare with the stored encoding
        match = face_recognition.compare_faces([d[name]], encs[0], tolerance=tolerance)
        return bool(match[0])
    except Exception as e:
        print(f"Verification failed: {e}")
        return False

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == 'enroll' and len(sys.argv) > 2:
            enroll_user(sys.argv[2])
        elif cmd == 'verify' and len(sys.argv) > 2:
            result = verify_user(sys.argv[2])
            print(f"Verification result: {result}")
            sys.exit(0 if result else 1)
        else:
            print("Usage: python camera_face_verify.py [enroll|verify] <username>")
    else:
        print("Usage: python camera_face_verify.py [enroll|verify] <username>")
