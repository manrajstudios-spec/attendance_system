import gc
import torch
from insightface.app import FaceAnalysis

face_model = FaceAnalysis(name="buffalo_l",providers=["CUDAExecutionProvider"])
det_threshold = 0.5


def prepare_modle():
    face_model.prepare(ctx_id=0,det_size=(640,640),det_thresh=det_threshold)

def unload_model():
    face_model.models.clear()
    gc.collect()

    if torch.cuda.is_available():
        torch.cuda.empty_cache()

def recognize_faces(cv_image):
    model_result = face_model.get(cv_image)
    
    if len(model_result) > 1:
        return "Multiple Faces Detected"
    
    if not model_result:
        return "No Faces Found"

    face_embedding = model_result[0].embedding
    
    return face_embedding