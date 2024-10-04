from flask import Flask, render_template, send_from_directory, request, jsonify
import os
from camera import crop_face
from flask_cors import CORS

app = Flask(__name__)
CORS(app) #allows all origins

# Path to the folder containing the images
FACES_FOLDER = 'faces'
app.config['UPLOAD_FOLDER'] = FACES_FOLDER

def get_latest_cropped_face():
    # List all files in the faces folder
    files = [f for f in os.listdir(FACES_FOLDER) if f.startswith('cropped_face') and f.endswith('.jpg')]
    if not files:
        return None
    
    # Get the latest file based on the numeric part of the filename
    latest_file = max(files, key=lambda x: int(x.split('_')[2].split('.')[0]))
    return latest_file

@app.route('/api/')
def index():
    return render_template('workingpage.html')

@app.route('/api/latest_cropped_face')
def latest_cropped_face_api():
    latest_cropped_face = get_latest_cropped_face()
    return jsonify({"latest_cropped_face": latest_cropped_face}) if latest_cropped_face else jsonify({"latest_cropped_face": None})

@app.route('/api/faces/<filename>')
def faces(filename):
    return send_from_directory(FACES_FOLDER, filename)

# IMAGE UPLOADS
@app.route('/api/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    
    image = request.files['image']
    
    if image.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    image_filename = f"uploaded_image_{len(os.listdir(FACES_FOLDER)) + 1}.jpg"
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
    image.save(image_path)
    
    # Crop the face using the crop_face() function from camera.py
    cropped_image_filename = f"cropped_face_{len(os.listdir(FACES_FOLDER)) + 1}.jpg"
    cropped_image_path = os.path.join(app.config['UPLOAD_FOLDER'], cropped_image_filename)
    
    if crop_face(image_path, cropped_image_path):  # Crop the image and save it
        return jsonify({"message": "Image uploaded and cropped successfully", "filename": cropped_image_filename}), 200
    else:
        return jsonify({"error": "No face detected in the image"}), 400

if __name__ == "__main__":
    if not os.path.exists(FACES_FOLDER):
        os.makedirs(FACES_FOLDER)
    app.run(debug=True, host="0.0.0.0")



