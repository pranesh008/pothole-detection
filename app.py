import os
from flask import Flask, request, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename
from ultralytics import YOLO
from moviepy import VideoFileClip  # Import MoviePy for video conversion
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'runs/detect'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Initialize the YOLO model
model_path = "E:/College/Pothole Detection/website/model.pt"
model = YOLO(model_path)

@app.route('/')
def index():
    return render_template('index.html')

def convert_to_mp4(input_path, output_path):
    """Convert video from .avi to .mp4 using MoviePy."""
    try:
        clip = VideoFileClip(input_path)
        clip.write_videofile(output_path, codec="libx264")
        clip.close()
    except Exception as e:
        print(f"Error converting video: {e}")
        raise e

@app.route('/upload_video', methods=['POST'])
def upload_video():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in request'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        # Save the uploaded video
        filename = secure_filename(file.filename)
        video_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(video_path)

        # Process the video
        result = model.predict(
            task='detect',
            mode='predict',
            model=model_path,
            source=video_path,
            save=True,
            save_dir=PROCESSED_FOLDER,
            conf=0.25
        )

        # Check for the latest directory in the 'runs/detect' folder
        subdirs = [os.path.join(PROCESSED_FOLDER, d) for d in os.listdir(PROCESSED_FOLDER) if os.path.isdir(os.path.join(PROCESSED_FOLDER, d))]
        latest_dir = max(subdirs, key=os.path.getmtime) if subdirs else PROCESSED_FOLDER
        print(f"Latest directory for processed files: {latest_dir}")

        # Find the processed video file in the latest directory
        processed_files = os.listdir(latest_dir)
        processed_video_path = None
        for file in processed_files:
            if file.endswith('.avi'):  # Look for .avi files
                processed_video_path = os.path.join(latest_dir, file)
                break

        if not processed_video_path:
            return jsonify({'error': 'Processed video not found!'}), 500

        print(f"Processed video path: {processed_video_path}")

        # Convert the video to .mp4
        mp4_video_path = processed_video_path.replace('.avi', '.mp4')
        convert_to_mp4(processed_video_path, mp4_video_path)

        # Check if the .mp4 video exists
        if not os.path.exists(mp4_video_path):
            return jsonify({'error': 'Video conversion to .mp4 failed!'}), 500

        print(f"Converted .mp4 video path: {mp4_video_path}")

        # Return the URL for the processed .mp4 video
        return jsonify({
            'message': 'Video processed successfully!',
            'download_url': f'/processed/{os.path.basename(latest_dir)}/{os.path.basename(mp4_video_path)}'
        })

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({'error': str(e)}), 500

# Serve processed videos
@app.route('/processed/<path:filename>')
def serve_processed_file(filename):
    try:
        return send_from_directory(PROCESSED_FOLDER, filename)
    except Exception as e:
        print(f"Error serving file: {e}")
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
