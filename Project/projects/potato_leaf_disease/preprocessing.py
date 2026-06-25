# Image preprocessing for the Potato-leaf CNN.
# The model embeds its own Resizing + Rescaling layers, so we only load the
# image, ensure RGB, resize, and return a batched float32 array of raw pixels.
from pathlib import Path

import numpy as np
from PIL import Image

IMAGE_SIZE = 256


# Return a (1, size, size, 3) float32 array for model inference.
def load_image_array(path: str | Path, size: int = IMAGE_SIZE) -> np.ndarray:
    with Image.open(path) as img:
        img = img.convert("RGB").resize((size, size))
        arr = np.asarray(img, dtype="float32")
    return np.expand_dims(arr, axis=0)
