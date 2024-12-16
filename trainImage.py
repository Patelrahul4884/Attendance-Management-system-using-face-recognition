import csv
import os, cv2
import numpy as np
import pandas as pd
import datetime
import time
from PIL import ImageTk, Image

# Train Image
def TrainImage(haarcasecade_path="haarcascade_frontalface_default.xml", 
               trainimage_path="TrainingImage", 
               trainimagelabel_path="TrainingImageLabel/Trainner.yml", 
               message=None, 
               text_to_speech=None):
    # Load the cascade classifier for face detection
    detector = cv2.CascadeClassifier(haarcasecade_path)
    
    # Get images and labels for training
    faces, Id = getImagesAndLables(trainimage_path)
    
    # Train the recognizer on the images and labels
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(faces, np.array(Id))
    
    # Save the trained model
    recognizer.save(trainimagelabel_path)
    
    # Inform the user about success
    res = "Image Trained successfully"
    if message is not None:
        message.configure(text=res)
    if text_to_speech is not None:
        text_to_speech(res)

def getImagesAndLables(path="TrainingImage"):
    # Ensure the directory exists
    if not os.path.exists(path):
        raise ValueError(f"Directory {path} does not exist.")
    
    # Get all subdirectories (each representing a person) inside the training image directory
    newdir = [os.path.join(path, d) for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    
    # Collect all image paths from the subdirectories
    imagePath = [
        os.path.join(d, f)
        for d in newdir
        for f in os.listdir(d)
        if f.endswith(".jpg") or f.endswith(".png")  # Specify the image file types
    ]
    
    faces = []
    Ids = []
    
    # Loop through each image file and prepare it for training
    for imagePath in imagePath:
        pilImage = Image.open(imagePath).convert("L")  # Convert image to grayscale
        imageNp = np.array(pilImage, "uint8")  # Convert the image to a numpy array
        try:
            # Extract Id from filename assuming format: 'subject_<id>.jpg'
            Id = int(os.path.split(imagePath)[-1].split("_")[1].split(".")[0])  
        except IndexError:
            print(f"Skipping invalid image: {imagePath}")
            continue
        
        faces.append(imageNp)
        Ids.append(Id)
    
    return faces, Ids
