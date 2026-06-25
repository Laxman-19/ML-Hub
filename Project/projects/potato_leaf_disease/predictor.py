# Predictor for the Potato-leaf disease image-classification project.
# TensorFlow is imported lazily inside load() so the hub starts instantly and
# only pays the import cost on the first image prediction.
import logging
from pathlib import Path

import numpy as np

from core.spec import PredictionResult

from .preprocessing import load_image_array

logger = logging.getLogger(__name__)
MODEL_PATH = Path(__file__).resolve().parent / "model" / "potatoes.h5"

# Class order matches tf image_dataset_from_directory (alphabetical).
CLASS_NAMES = ["Early Blight", "Late Blight", "Healthy"]

_ADVICE = {"Early Blight": "Early blight detected - consider fungicide and remove affected foliage.",
           "Late Blight": "Late blight detected - act quickly; it spreads fast in cool, wet conditions.",
           "Healthy": "Leaf appears healthy - no disease signs detected."}


# Load the Keras CNN (called once, then cached by the hub).
def load():
    import tensorflow as tf
    logger.info("Loading Potato CNN from %s", MODEL_PATH)
    return tf.keras.models.load_model(MODEL_PATH, compile=False)


def predict(model, inputs):
    preds = model.predict(load_image_array(inputs["image"]), verbose=0)[0]
    idx = int(np.argmax(preds))
    label = CLASS_NAMES[idx] if idx < len(CLASS_NAMES) else f"Class {idx}"
    probabilities = {CLASS_NAMES[i] if i < len(CLASS_NAMES) else f"Class {i}": round(float(p) * 100, 2)
                     for i, p in enumerate(preds)}
    return PredictionResult(label=label, confidence=float(np.max(preds)),
                            detail=_ADVICE.get(label, ""), extra={"probabilities": probabilities})
