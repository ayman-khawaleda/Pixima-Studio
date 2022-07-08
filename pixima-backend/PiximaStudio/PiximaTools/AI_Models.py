import mediapipe as mp

mp_face_detection = mp.solutions.face_detection

face_detection_modle = mp_face_detection.FaceDetection(
    model_selection=1, min_detection_confidence=0.5
)
