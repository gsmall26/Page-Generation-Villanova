import cv2

cap = cv2.VideoCapture(0)  #VideoCapture object to access camera, 0 for default

while True:
    ret, frame = cap.read() #ret is boolean about success, frame is actual data

    # Display the resulting frame
    cv2.imshow('Camera', frame)

    key = cv2.waitKey(1)
    if key == ord('s'):

        cv2.imwrite('captured_image.jpg', frame) #save capture as captured_image.jpg in current directory
        img = cv2.imread('captured_image.jpg') #stores image in variable

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #grayscale

        # Load the pre-trained Haar Cascade face detection model
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Detect faces in the image
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5) #represents a rectange that encloses a detected face
        #higher scalefactor (>1) reduces sensitivity, look for faces in larger areas. lower (<1) increases sensitivity, look for faces in smaller areas.
        #neighbors are number of overlapping rectangles required to consider a region as valid. higher minNeighbors reduces false positives but can miss some. lower minNeighbors detects more faces but can lead to false positives

        # If a face is detected, crop and save the first detected face
        if len(faces) > 0:
            (x, y, w, h) = faces[0] #get coordinates of the rectangle that encloses the detected face. (x, y) top left corner. (w,h) width and height
            cropped_face = img[y:y + h, x:x + w] #extracts ROI from initial image with color
            cv2.imwrite('cropped_face.jpg', cropped_face)
            print('Face cropped and saved as cropped_face.jpg')
        else:
            print('No faces detected.')

        break

    elif key == ord('q'):
        break

# Release the VideoCapture object and close all windows
cap.release()
cv2.destroyAllWindows()