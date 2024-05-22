import time

from celery import shared_task
from celery import Task

from PIL import Image
import numpy as np

import os

os.environ["KERAS_BACKEND"] = "tensorflow"

import keras  # noqa: E402


@shared_task(ignore_result=False)
def predict(image_paths: list[str]) -> list[str]:
    model = keras.saving.load_model("model.keras")

    results = []

    for image_path in image_paths:
        image = Image.open(image_path)
        image_array = np.array(image) / 255.0
        image_array = np.expand_dims(image_array, axis=0)

        predictions = model.predict(image_array)
        class_names = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        predicted_class = class_names[np.argmax(predictions)]

        results.append(predicted_class)

        os.remove(image_path)
    return results
