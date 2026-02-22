import cv2
import dlib
import numpy as np

# Load pre-trained face detector and landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Function to calculate the Euclidean distance
def euclidean_distance(pt1, pt2):
    return np.linalg.norm(np.array(pt1) - np.array(pt2))

# Function to detect and classify face shape
def detect_face_shape(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    faces = detector(gray)
    
    if len(faces) == 0:
        return "No face detected"
    
    for face in faces:
        landmarks = predictor(gray, face)

        # Extract key points
        jaw_width = euclidean_distance((landmarks.part(0).x, landmarks.part(0).y),
                                       (landmarks.part(16).x, landmarks.part(16).y))
        forehead_width = euclidean_distance((landmarks.part(19).x, landmarks.part(19).y),
                                            (landmarks.part(24).x, landmarks.part(24).y))
        face_length = euclidean_distance((landmarks.part(8).x, landmarks.part(8).y),
                                         (landmarks.part(27).x, landmarks.part(27).y))

        # Classify face shape
        if face_length > jaw_width and jaw_width > forehead_width:
            return "Oval Face"
        elif jaw_width > face_length and jaw_width > forehead_width:
            return "Square Face"
        elif forehead_width > jaw_width and forehead_width > face_length:
            return "Heart Face"
        elif face_length > jaw_width and face_length > forehead_width:
            return "Oblong Face"
        else:
            return "Round Face"

# Example usage
image_path = "face.jpg"  # Replace with an actual image path
face_shape = detect_face_shape(image_path)
print("Detected Face Shape:", face_shape)
