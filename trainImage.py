import csv
import os
import cv2
import numpy as np
from PIL import Image


def TrainImage(haarcasecade_path, trainimage_path, trainimagelabel_path, message, text_to_speech):
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        haarcasecade_path = os.path.join(BASE_DIR, haarcasecade_path)
        trainimage_path = os.path.join(BASE_DIR, trainimage_path)
        trainimagelabel_path = os.path.join(BASE_DIR, trainimagelabel_path)

        os.makedirs(trainimage_path, exist_ok=True)
        os.makedirs(os.path.dirname(trainimagelabel_path), exist_ok=True)

        recognizer = cv2.face.LBPHFaceRecognizer_create()
        detector = cv2.CascadeClassifier(haarcasecade_path)

        faces, Id = getImagesAndLables(trainimage_path)
        if len(faces) == 0:
            raise Exception("No face images found for training!")

        recognizer.train(faces, np.array(Id))
        recognizer.save(trainimagelabel_path)

        res = "Images Trained Successfully"
        message.configure(text=res)
        text_to_speech(res)

    except Exception as e:
        res = f"Training Failed: {str(e)}"
        message.configure(text=res)
        text_to_speech(res)


def getImagesAndLables(path):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(BASE_DIR, path)

    faces = []
    Ids = []

    if not os.path.exists(path):
        raise Exception(f"Training image path does not exist: {path}")

    # Get subdirectories (student folders)
    directories = [os.path.join(path, d) for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

    for directory in directories:
        imageFiles = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".jpg")]
        for imagePath in imageFiles:
            pilImage = Image.open(imagePath).convert("L")  # convert to grayscale
            imageNp = np.array(pilImage, "uint8")

            try:
                Id = int(os.path.split(imagePath)[-1].split("_")[1])
            except Exception:
                continue  # skip files that do not match pattern

            faces.append(imageNp)
            Ids.append(Id)

    return faces, Ids
