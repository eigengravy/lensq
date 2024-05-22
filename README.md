# lensq

lensq is a application that provides an API for predicting handwritten digits using a pre-trained deep learning model.

Built w/ Flask, Keras and Celery.

## Setup Development Environment

1. Clone the repository:

```sh
git clone https://github.com/your-username/lensq.git
cd lensq
```

2. Install dependencies and drop into `env` shell:

```sh
poetry install
poetry shell
```

3. Download the pre-trained model weights file `model.keras` and place it in the project root directory. Alternatively, you can train it locally using `scripts/train.py`.

## Model

The application uses a pre-trained CNN model for handwritten digit recognition. The model is trained on the MNIST dataset and achieves an accuracy of around 99% on the test set.

The pre-trained weights `model.keras` are required to run the application. You can download the weights file from the project repository or train the model yourself using the provided `train.py` script.

## Running the Application Locally

1. Spin up a `redis` instance using `docker run` on port `6379`. Alternatively, you can run `redis` locally.

```sh
docker run -d -p 6379:6379 redis 
```

2. Start the `celery` worker.

```
celery -A make_celery worker --loglevel INFO  
```

3. In a separate terminal, start the Flask application:

```sh
flask -A lensq run --debug
```

The application should now be accessible at `http://localhost:5000`.

## Deploying to Server

To deploy the application to a server environment, follow these steps:

1. Setup an EC2 instance and install required dependencies (Redis, Celery, Flask) on the server.
2. Clone the repository and copy the project files to the server.
3. Place the pre-trained model weights file `model.keras` in the project root directory.
4. Configure the Redis and Celery settings in `lensq/__init__.py` as per your server environment.
5. Start the Redis server.
6. Start the Celery worker.
7. Start the Flask application using Gunicorn.

`pm2` is used to manage the `celery` and `flask` jobs.

## API Documentation

### Endpoint: `/tasks/predict`

**Method**: POST

**Input Parameters**:

- `images` (multipart/form-data): One or more image files to be processed for digit recognition.

**Response**:

```json
{
    "result_id": "string"
}
```

The `result_id` is a unique identifier for the submitted task. It can be used to check the status and retrieve the prediction results.

### Endpoint: `/tasks/result/<id>`

**Method**: GET

**Path Parameter**:

- `id` (string): The `result_id` returned by the `/tasks/predict` endpoint.

**Response**:

```json
{
    "ready": bool,
    "successful": bool,
    "value": list
}
```

- `ready`: Indicates whether the prediction task has completed.
- `successful`: Indicates whether the prediction task was successful (only present when `ready` is `true`).
- `value`: A list of predicted digit labels for each submitted image (only present when `ready` and `successful` are `true`).
