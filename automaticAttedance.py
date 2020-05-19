import tkinter as tk
from tkinter import Message, Text
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


haarcasecade_path = "C:\\Users\\patel\\OneDrive\\Documents\\E\\FBAS\\haarcascade_frontalface_default.xml"
trainimagelabel_path = (
    "C:\\Users\\patel\\OneDrive\\Documents\\E\\FBAS\\TrainingImageLabel\\Trainner.yml"
)
trainimage_path = "C:\\Users\\patel\\OneDrive\\Documents\\E\\FBAS\\TrainingImage"
studentdetail_path = (
    "C:\\Users\\patel\\OneDrive\\Documents\\E\\FBAS\\StudentDetails\\studentdetails.csv"
)
attendance_path = "C:\\Users\\patel\\OneDrive\\Documents\\E\\FBAS\\Attendance"
# for choose subject and fill attendance
def subjectChoose(err_screen1):
    def FillAttendance():
        sub = tx.get()
        now = time.time()
        future = now + 20
        print(now)
        print(future)
        if time.time() < future:
            if sub == "":
                err_screen1()
            else:
                recognizer = cv2.face.LBPHFaceRecognizer_create()
                try:
                    recognizer.read(trainimagelabel_path)
                except:
                    e = "Model not found,please train model"
                    Notifica.configure(
                        text=e,
                        bg="Grey",
                        fg="white",
                        width=33,
                        font=("times", 15, "bold"),
                    )
                    Notifica.place(x=20, y=250)
                facecasCade = cv2.CascadeClassifier(haarcasecade_path)
                df = pd.read_csv(studentdetail_path)
                cam = cv2.VideoCapture(0)
                font = cv2.FONT_HERSHEY_SIMPLEX
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
                            date = datetime.datetime.fromtimestamp(ts).strftime(
                                "%Y-%m-%d"
                            )
                            timeStamp = datetime.datetime.fromtimestamp(ts).strftime(
                                "%H:%M:%S"
                            )
                            aa = df.loc[df["Enrollment"] == Id]["Name"].values
                            global tt
                            tt = str(Id) + "-" + aa
                            # En='1604501160'+str(Id)
                            attendance.loc[len(attendance)] = [
                                Id,
                                aa,
                            ]
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 4)
                            cv2.putText(
                                im, str(tt), (x + h, y), font, 1, (255, 255, 0,), 4
                            )
                        else:
                            Id = "Unknown"
                            tt = str(Id)
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                            cv2.putText(
                                im, str(tt), (x + h, y), font, 1, (0, 25, 255), 4
                            )
                    if time.time() > future:
                        break

                    attendance = attendance.drop_duplicates(
                        ["Enrollment"], keep="first"
                    )
                    cv2.imshow("Filling Attendance...", im)
                    key = cv2.waitKey(30) & 0xFF
                    if key == 27:
                        break

                ts = time.time()
                print(aa)
                # attendance["date"] = date
                # attendance["Attendance"] = "P"
                attendance[date] = 1
                date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
                Hour, Minute, Second = timeStamp.split(":")
                # fileName = "Attendance/" + Subject + ".csv"
                path = os.path.join(attendance_path, Subject)
                fileName = (
                    f"{path}/"
                    + Subject
                    + "_"
                    + date
                    + "_"
                    + Hour
                    + "-"
                    + Minute
                    + "-"
                    + Second
                    + ".csv"
                )
                attendance = attendance.drop_duplicates(["Enrollment"], keep="first")
                print(attendance)
                attendance.to_csv(fileName, index=False)

                m = "Attendance Filled Successfully"
                Notifica.configure(
                    text=m, bg="Grey", fg="white", width=33, font=("times", 15, "bold")
                )
                Notifica.place(x=20, y=250)

                cam.release()
                cv2.destroyAllWindows()

                import csv
                import tkinter

                root = tkinter.Tk()
                root.title("Attendance of " + Subject)
                root.configure(background="snow")
                cs = os.path.join(path, fileName)
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
                                fg="black",
                                font=("times", 15, " bold "),
                                bg="lawn green",
                                text=row,
                                relief=tkinter.RIDGE,
                            )
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                root.mainloop()
                print(attendance)

    ###windo is frame for subject chooser
    windo = tk.Tk()
    # windo.iconbitmap("AMS.ico")
    windo.title("Enter subject name...")
    windo.geometry("580x320")
    windo.configure(background="snow")
    Notifica = tk.Label(
        windo,
        text="Attendance filled Successfully",
        bg="grey",
        fg="white",
        width=33,
        height=2,
        font=("times", 15, "bold"),
    )

    def Attf():
        import subprocess

        subprocess.Popen(
            r'explorer \\select,"C:\\Users\\patel\\OneDrive\Documents\\E\\FBAS\\"'
        )

    attf = tk.Button(
        windo,
        text="Check Sheets",
        command=Attf,
        fg="white",
        bg="grey",
        width=12,
        height=1,
        activebackground="Red",
        font=("times", 14, " bold "),
    )
    attf.place(x=430, y=255)

    sub = tk.Label(
        windo,
        text="Enter Subject",
        width=15,
        height=2,
        fg="white",
        bg="grey",
        font=("times", 15, " bold "),
    )
    sub.place(x=30, y=100)

    tx = tk.Entry(windo, width=20, bg="grey", fg="white", font=("times", 23, " bold "))
    tx.place(x=250, y=105)

    fill_a = tk.Button(
        windo,
        text="Fill Attendance",
        fg="white",
        command=FillAttendance,
        bg="grey",
        width=20,
        height=2,
        activebackground="Red",
        font=("times", 15, " bold "),
    )
    fill_a.place(x=250, y=160)
    windo.mainloop()