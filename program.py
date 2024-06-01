import face_recognition
import cv2
import numpy as np
import csv
from datetime import datetime

# Load known face encodings and names
ashish_image = face_recognition.load_image_file("photos/ashish.jpg")
ashish_encoding = face_recognition.face_encodings(ashish_image)[0]

hiran_image = face_recognition.load_image_file("photos/hiran.jpg")
hiran_encoding = face_recognition.face_encodings(hiran_image)[0]

pratyush_image = face_recognition.load_image_file("photos/pratyush.jpg")
pratyush_encoding = face_recognition.face_encodings(pratyush_image)[0]

known_face_encodings = [
    ashish_encoding,
    hiran_encoding,
    pratyush_encoding
]

known_face_names = [
    "ashish",
    "hiran",
    "pratyush"
]

# Open a CSV file to store attendance
now = datetime.now()
current_date = now.strftime("%Y-%m-%d")
csv_file_path = current_date + '.csv'
csv_file = open(csv_file_path, 'w', newline='')
csv_writer = csv.writer(csv_file)

# Initialize video capture
video_capture = cv2.VideoCapture(0)

recognized_names = []

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    
    # Resize the frame to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    
    # Convert the frame to RGB for face recognition
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
    
    # Find all face locations and encodings in the current frame
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    
    # Initialize an empty list to store the names of recognized faces
    face_names = []
    
    # Iterate through each detected face
    for face_encoding in face_encodings:
        # Compare the current face encoding with known face encodings
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        
        # Check if there is a match
        if True in matches:
            # Find the index of the first match and use it to get the corresponding name
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
        
        # Add the recognized name to the list
        face_names.append(name)
        
        # Write attendance to CSV if the recognized name is in the known face names
        if name in known_face_names and name not in recognized_names:
            current_time = now.strftime("%H-%M-%S")
            csv_writer.writerow([name, current_time])
            recognized_names.append(name)

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a rectangle around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting frame
    cv2.imshow('Attendance System', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and close CSV file
video_capture.release()
csv_file.close()

# Close all OpenCV windows
cv2.destroyAllWindows()

