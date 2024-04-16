from flask import Flask, render_template, request
import cv2
import os
app = Flask(__name__)

@app.route('/')
def index():
    image_path = './image.png'
    return render_template('index.html', image_path=image_path)

# @app.route('/upload', methods=['POST'])
# def upload():
#     if request.method == 'POST':
#         # Capture snapshot using OpenCV
#         camera = cv2.VideoCapture(0)
#         _, image = camera.read()
#         camera.release()

#         # Save the snapshot
#         cv2.imwrite('static/snapshot.jpg', image)
        
#         return render_template('result.html')



if __name__ == '__main__':
    app.run(debug=True)
