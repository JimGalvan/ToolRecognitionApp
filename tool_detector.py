from fastai.vision.all import *


class ToolDetector:
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.learn = load_learner(model_path)

    def predict(self, image):
        img = PILImage.create(image)
        pred_mask, _, _ = self.learn.predict(img)
