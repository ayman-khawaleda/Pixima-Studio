from abc import ABC, abstractmethod
import mediapipe as mp
import keras as ke
import numpy as np
from PiximaStudio.settings import PROJECT_DIR
import os
from mediapipe.python.solutions.drawing_utils import DrawingSpec
from mediapipe.python.solutions.drawing_utils import draw_landmarks
mp_face_detection = mp.solutions.face_detection
mp_face_mesh = mp.solutions.face_mesh
mp_drawing_styles = mp.solutions.drawing_styles

face_detection_model = mp_face_detection.FaceDetection(
    model_selection=1, min_detection_confidence=0.5
)

face_mesh_model = mp_face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
)

class AIModel(ABC):
    @classmethod
    @abstractmethod
    def load_model(self,path):
        pass
    
    @classmethod
    @abstractmethod
    def predict(self,input):
        pass
    
class DNNModel(AIModel):
    pass

class FaceSegmentationModel(DNNModel):
    def __init__(self,path=os.path.join(PROJECT_DIR,"DNN_Models/FaceSeg-Model.h5")):
        self.model = ke.models.load_model(path)

    def load_model(self,path=os.path.join(PROJECT_DIR,"DNN_Models/FaceSeg-Model.h5")):
        self.model = ke.models.load_model(path)

    def predict(self,input):
        "Input <Gray Image> Should Have shape like (256,256,1)"
        return self.model.predict(np.asarray([input])).reshape((256,256))
