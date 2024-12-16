import tkinter as tk
from tkinter import *
import os, cv2
import shutil
import csv
import numpy as np
from PIL import ImageTk, Image
import pandas as pd
import datetime
import time
import tkinter.ttk as tkk
import tkinter.font as font

# Define the paths for various files and directories
haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = "TrainingImageLabel/Trainner.yml"
trainimage_path = "TrainingImage"
studentdetail_path = "StudentDetails/studentdetails.csv"
attendance_path = "Attendance"

# Function to choose subject and fill attendance
def subjectChoose(text_to_speech):
    def FillAttendance():
        sub = tx.get()
        now = time.time()
        future = now + 20
        print(now)
        print(future)
        
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            try:
                # Attempt to read the trained model
                recognizer = cv2.face.LBPHFaceRecognizer_create()
                try:
                    recognizer.read(trainimagelabel_path)
                except:
                    e = "Model not found, please train model"
                    Notifica.configure(
                        text=e,
                        bg="black",
                        fg="yellow",
                        width=33,
                        font=("times", 15, "bold"),
                    )
                    Notifica.place(x=20, y=250)
                    text_to_speech(e)

                # Load the face detection classifier
                facecasCade = cv2.CascadeClassifier(haarcasecade_path)
                df = pd.read_csv(studentdetail_path)
                cam = cv2.VideoCapture(0)
                font = cv2.FONT_HERSHEY_SIMPLEX

                # Prepare the DataFrame for attendance
                col_names = ["Enrollment", "Name"]
                attendance = pd.DataFrame(columns=col_names)
                
                while True:
                    ___, im = cam.read()
                    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                    faces = facecasCade.detectMultiScale(gray, 1.2, 5)
                    for (x, y, w, h) in faces:
                        global Id

                        Id, conf = recognizer.predict(gray[y : y + h, x : x + w])
                        if conf < 70:
                            print(conf)
                            global Subject
                            global aa
                            global date
                            global timeStamp
                            Subject = tx.get()
                            ts = time.time()
                            date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                            timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
                            aa = df.loc[df["Enrollment"] == Id]["Name"].values
                            global tt
                            tt = str(Id) + "-" + aa
                            
                            attendance.loc[len(attendance)] = [Id, aa]
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 4)
                            cv2.putText(im, str(tt), (x + h, y), font, 1, (255, 255, 0,), 4)
                        else:
                            Id = "Unknown"
                            tt = str(Id)
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                            cv2.putText(im, str(tt), (x + h, y), font, 1, (0, 25, 255), 4)

                    if time.time() > future:
                        break

                    attendance = attendance.drop_duplicates(["Enrollment"], keep="first")
                    cv2.imshow("Filling Attendance...", im)
                    key = cv2.waitKey(30) & 0xFF
                    if key == 27:
                        break

                ts = time.time()
                attendance[date] = 1
                date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
                Hour, Minute, Second = timeStamp.split(":")
                
                # Define the path where attendance will be saved
                path = os.path.join(attendance_path, sub)
                if not os.path.exists(path):
                    os.makedirs(path)

                # File name with timestamp
                fileName = f"{path}/{sub}_{date}_{Hour}-{Minute}-{Second}.csv"
                
                # Remove duplicate entries before saving
                attendance = attendance.drop_duplicates(["Enrollment"], keep="first")
                attendance.to_csv(fileName, index=False)

                m = f"Attendance Filled Successfully for {sub}"
                Notifica.configure(
                    text=m,
                    bg="black",
                    fg="yellow",
                    width=33,
                    relief=RIDGE,
                    bd=5,
                    font=("times", 15, "bold"),
                )
                text_to_speech(m)
                Notifica.place(x=20, y=250)

                cam.release()
                cv2.destroyAllWindows()

                # Display the attendance in a Tkinter window
                root = tkinter.Tk()
                root.title(f"Attendance of {sub}")
                root.configure(background="black")
                
                # Read and display the saved attendance CSV file
                cs = os.path.join(path, f"{sub}_{date}_{Hour}-{Minute}-{Second}.csv")
                print(cs)
                with open(cs, newline="") as file:
                    reader = csv.reader(file)
                    r = 0
                    for col in reader:
                        c = 0
                        for row in col:
                            label = tkinter.Label(
                                root,
                                width=10,
                                height=1,
                                fg="yellow",
                                font=("times", 15, " bold "),
                                bg="black",
                                text=row,
                                relief=tkinter.RIDGE,
                            )
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                root.mainloop()

            except:
                f = "No Face found for attendance"
                text_to_speech(f)
                cv2.destroyAllWindows()

    # GUI setup
    subject = Tk()
    subject.title("Subject...")
    subject.geometry("580x320")
    subject.resizable(0, 0)
    subject.configure(background="black")
    
    titl = tk.Label(subject, bg="black", relief=RIDGE, bd=10, font=("arial", 30))
    titl.pack(fill=X)

    titl = tk.Label(
        subject,
        text="Enter the Subject Name",
        bg="black",
        fg="green",
        font=("arial", 25),
    )
    titl.place(x=160, y=12)
    
    Notifica = tk.Label(
        subject,
        text="Attendance filled Successfully",
        bg="yellow",
        fg="black",
        width=33,
        height=2,
        font=("times", 15, "bold"),
    )

    def Attf():
        sub = tx.get()
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            subject_dir = os.path.join(attendance_path, sub)
            if os.path.exists(subject_dir):
                os.startfile(subject_dir)
            else:
                t = f"The folder for subject '{sub}' does not exist."
                text_to_speech(t)

    attf = tk.Button(
        subject,
        text="Check Sheets",
        command=Attf,
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="yellow",
        height=2,
        width=10,
        relief=RIDGE,
    )
    attf.place(x=360, y=170)

    sub = tk.Label(
        subject,
        text="Enter Subject",
        width=10,
        height=2,
        bg="black",
        fg="yellow",
        bd=5,
        relief=RIDGE,
        font=("times new roman", 15),
    )
    sub.place(x=50, y=100)

    tx = tk.Entry(
        subject,
        width=15,
        bd=5,
        bg="black",
        fg="yellow",
        relief=RIDGE,
        font=("times", 30, "bold"),
    )
    tx.place(x=190, y=100)

    fill_a = tk.Button(
        subject,
        text="Fill Attendance",
        command=FillAttendance,
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="yellow",
        height=2,
        width=12,
        relief=RIDGE,
    )
    fill_a.place(x=195, y=170)

    subject.mainloop()
