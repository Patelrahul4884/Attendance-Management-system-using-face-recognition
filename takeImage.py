import csv
import os
import cv2
import numpy as np
import pandas as pd
import datetime
import time

# take Image of user
def TakeImage(l1, l2, haarcasecade_path="haarcascade_frontalface_default.xml", 
              trainimage_path="TrainingImage", message=None, err_screen=None, 
              text_to_speech=None):
    if (l1 == "") and (l2 == ""):
        t = 'Please Enter your Enrollment Number and Name.'
        text_to_speech(t)
    elif l1 == '':
        t = 'Please Enter your Enrollment Number.'
        text_to_speech(t)
    elif l2 == "":
        t = 'Please Enter your Name.'
        text_to_speech(t)
    else:
        try:
            # Initialize the webcam
            cam = cv2.VideoCapture(0)
            # Load the face detection model
            detector = cv2.CascadeClassifier(haarcasecade_path)
            
            # Store user info
            Enrollment = l1
            Name = l2
            sampleNum = 0
            
            # Create directory for user images
            directory = f"{Enrollment}_{Name}"
            path = os.path.join(trainimage_path, directory)
            
            # Check if the directory already exists
            if not os.path.exists(path):
                os.mkdir(path)
            
            # Capture 50 images of the user
            while True:
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                
                # Loop over all faces detected
                for (x, y, w, h) in faces:
                    # Draw rectangle around face
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    sampleNum += 1
                    # Save the captured image
                    cv2.imwrite(
                        os.path.join(path, f"{Name}_{Enrollment}_{sampleNum}.jpg"),
                        gray[y:y + h, x:x + w]
                    )
                    # Display image
                    cv2.imshow("Frame", img)
                
                # Exit when 'q' is pressed or after 50 images
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
                elif sampleNum >= 50:
                    break
            
            # Release the webcam and close the window
            cam.release()
            cv2.destroyAllWindows()
            
            # Save student details into CSV
            row = [Enrollment, Name]
            student_details_path = "StudentDetails/studentdetails.csv"
            
            # Check if the directory exists
            if not os.path.exists("StudentDetails"):
                os.makedirs("StudentDetails")
            
            with open(student_details_path, "a+") as csvFile:
                writer = csv.writer(csvFile, delimiter=",")
                writer.writerow(row)
                csvFile.close()
            
            # Success message
            res = f"Images Saved for ER No: {Enrollment} Name: {Name}"
            message.configure(text=res)
            text_to_speech(res)
        
        except FileExistsError as F:
            error_message = "Student Data already exists"
            text_to_speech(error_message)

