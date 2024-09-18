from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

# Path to the folder containing the images
FACES_FOLDER = 'faces'

def get_latest_cropped_face():
    # List all files in the faces folder
    files = [f for f in os.listdir(FACES_FOLDER) if f.startswith('cropped_face') and f.endswith('.jpg')]
    if not files:
        return None
    
    # Get the latest file based on the numeric part of the filename
    latest_file = max(files, key=lambda x: int(x.split('_')[2].split('.')[0]))
    return latest_file

@app.route('/')
def index():
    latest_cropped_face = get_latest_cropped_face()
    print(latest_cropped_face)
    return render_template('workingpage.html', latest_cropped_face=latest_cropped_face)

@app.route('/faces/<filename>')
def faces(filename):
    return send_from_directory(FACES_FOLDER, filename)

# if __name__ == '__main__':
#     app.run(debug=True)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")