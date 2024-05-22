import os
import uuid
from celery.result import AsyncResult
from flask import Blueprint
from flask import request

from . import tasks

bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@bp.get("/result/<id>")
def result(id: str) -> dict[str, object]:
    result = AsyncResult(id)
    ready = result.ready()
    return {
        "ready": ready,
        "successful": result.successful() if ready else None,
        "value": result.get() if ready else result.result,
    }


@bp.post("/predict")
def predict() -> dict[str, object]:
    images = request.files.getlist("images")
    image_paths = []
    for image in images:
        image_path = os.path.join("tmp", f"{uuid.uuid4().hex}.jpg")
        os.makedirs("tmp", exist_ok=True)
        image.save(image_path)
        image_paths.append(image_path)
    result = tasks.predict.delay(image_paths)
    return {"result_id": result.id}
