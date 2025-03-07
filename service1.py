from datetime import datetime
import cv2
import numpy as np
import face_recognition
import os
import tensorflow as tf

# Set up TensorBoard logging
logdir = "logs/attendance_logs"
os.makedirs(logdir, exist_ok=True)  # Create the log directory if it doesn't exist
writer = tf.summary.create_file_writer(logdir)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
face_data_dir = ROOT + "/face_data"

def recognize_faces():
    global Id
    images = []
    classNames = []

    # Load images and face IDs from the face_data directory
    for filename in os.listdir(face_data_dir):
        if filename.startswith("User"):
            img = cv2.imread(os.path.join(face_data_dir, filename), cv2.IMREAD_GRAYSCALE)
            face_id = int(filename.split(".")[1])
            images.append(img)
            classNames.append(face_id)

    # Function to find face encodings
    def findEncodings(images):
        encodeList = []
        for img in images:
            try:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                encode = face_recognition.face_encodings(img)[0]
                encodeList.append(encode)
            except:
                pass
        return encodeList

    # Get known face encodings
    encodeListKnown = findEncodings(images)

    cap = cv2.VideoCapture(0)

    while True:
        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                Id = classNames[matchIndex]

                # Calculate accuracy (lower distance means higher accuracy)
                accuracy = 1 - faceDis[matchIndex]
                
                # Log the accuracy using TensorBoard
                with writer.as_default():
                    tf.summary.scalar("Face Recognition Accuracy", accuracy, step=int(Id))

                # Display the recognized face with a rectangle and ID
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, str(Id), (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow('Webcam', img)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return Id

# Call the function to start face recognition and logging
recognize_faces()