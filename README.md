# Pothole Detection App using YOLOv8

## Overview

This is a Flask-based application that detects potholes in video clips using the YOLOv8 model. Users can upload videos, and the application processes them to detect potholes, returning a downloadable processed video with bounding boxes highlighting the detected potholes. The static frontend is hosted on Fly.io, and the backend handles model inference and video processing.

## Features

- Upload video files for pothole detection.
- Utilizes the YOLOv8 model for detection.
- Converts processed AVI videos to MP4 format.
- Serves processed videos for download.
- CORS enabled for seamless frontend-backend communication.

## Tech Stack

- **Backend:** Python, Flask
- **Machine Learning:** YOLOv8 (Ultralytics)
- **Video Processing:** MoviePy
- **Deployment:** Fly.io (Frontend), Local/Cloud (Backend)

## Installation

### Prerequisites

Ensure you have the following installed:

- Python 3.8+
- Pip
- Virtual Environment (optional but recommended)

### Clone the Repository

```sh
git clone https://github.com/yourusername/pothole-detection-app.git
cd pothole-detection-app
```

### Set Up a Virtual Environment (Optional)

```sh
python -m venv venv
source venv/bin/activate   # On Windows use `venv\Scripts\activate`
```

### Install Dependencies

```sh
pip install -r requirements.txt
```

## Model Setup

Ensure you have the trained YOLOv8 model (`model.pt`) and update its path in `app.py`:

```python
model_path = "E:/College/Pothole Detection/website/model.pt"  # Update as needed
model = YOLO(model_path)
```

## Running the Application

Start the Flask server:

```sh
python app.py
```

The backend will be available at `http://localhost:5000`.

## API Endpoints

### 1. Upload Video

**Endpoint:** `POST /upload_video`

- **Description:** Uploads a video and processes it using the YOLOv8 model.
- **Request:**
  - `file` (multipart/form-data): Video file to be processed.
- **Response:** JSON containing the processed video's download URL.

### 2. Serve Processed Videos

**Endpoint:** `GET /processed/<filename>`

- **Description:** Serves processed videos stored in `runs/detect/`.

## Deployment

### Fly.io (Frontend Hosting)

1. Install Fly CLI:
   ```sh
   curl -fsSL https://fly.io/install.sh | sh
   ```
2. Login and create an app:
   ```sh
   flyctl auth login
   flyctl launch
   ```
3. Deploy:
   ```sh
   flyctl deploy
   ```

## Future Improvements

- Enhance detection accuracy by training with more datasets.
- Implement real-time detection using live camera feed.
- Improve UI/UX for better user experience.

## License

This project is open-source and available under the MIT License.

---

**Author:** Pranesh Puri
**GitHub:** pranesh008 (https://github.com/pranesh008/)

