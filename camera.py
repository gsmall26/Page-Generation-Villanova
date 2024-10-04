import cv2
import os

faces_folder = "faces"

# Ensure the "faces" folder exists
if not os.path.exists(faces_folder):
    os.makedirs(faces_folder)

# Refactor the face cropping part into a reusable function
def crop_face(image_path, save_path):
    # Load the image
    frame = cv2.imread(image_path)
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Load the pre-trained Haar Cascade face detection model
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    #higher scalefactor (>1) reduces sensitivity, look for faces in larger areas. lower (<1) increases sensitivity, look for faces in smaller areas.
    #neighbors are number of overlapping rectangles required to consider a region as valid. higher minNeighbors reduces false positives but can miss some. lower minNeighbors detects more faces but can lead to false positives

    # If a face is detected, crop and save the first detected face
    if len(faces) > 0:
        (x, y, w, h) = faces[0]  # Get coordinates of the rectangle that encloses the detected face
        cropped_face = frame[y:y + h, x:x + w]  # Extracts ROI from the image

        # Save the cropped face
        cv2.imwrite(save_path, cropped_face)
        print(f'Face cropped and saved as {save_path}')
        return True
    else:
        print('No faces detected.')
        return False

# Function to capture a picture using the device's camera
def capture_and_crop_image():
    cap = cv2.VideoCapture(0)  # 0 for the default camera
    
    # Get the current image count by checking the number of images in the faces folder
    existing_images = [f for f in os.listdir(faces_folder) if f.startswith('cropped_face') and f.endswith('.jpg')]
    image_count = len(existing_images)

    while True:
        ret, frame = cap.read() #ret is boolean about success, frame is actual data

        # Display the resulting frame
        cv2.imshow('Camera', frame)

        key = cv2.waitKey(1)
        if key == ord('s'):
            # Save and crop the captured image
            full_image_filename = f'captured_image_{image_count}.jpg'
            image_path = os.path.join(faces_folder, full_image_filename)
            cv2.imwrite(image_path, frame)

            # Perform face cropping
            cropped_face_filename = os.path.join(faces_folder, f'cropped_face_{image_count}.jpg')
            crop_face(image_path, cropped_face_filename)
            
            image_count += 1
            break
        elif key == ord('q'):
            break

    # Release the VideoCapture object and close all windows
    cap.release()
    cv2.destroyAllWindows()
