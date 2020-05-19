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

# project module
import show_attendance
import takeImage
import trainImage
import automaticAttedance

haarcasecade_path = "C:\\Users\\patel\\OneDrive\\Documents\\E\\FBAS\\haarcascade_frontalface_default.xml"
trainimagelabel_path = (
    "C:\\Users\\patel\\OneDrive\\Documents\\E\\FBAS\\TrainingImageLabel\\Trainner.yml"
)
trainimage_path = "C:\\Users\\patel\\OneDrive\\Documents\\E\\FBAS\\TrainingImage"
studentdetail_path = (
    "C:\\Users\\patel\\OneDrive\\Documents\\E\\FBAS\\StudentDetails\\studentdetails.csv"
)
attendance_path = "C:\\Users\\patel\\OneDrive\\Documents\\E\\FBAS\\Attendance"

window = tk.Tk()
window.title("Face recognizer")
window.geometry("1024x768")
dialog_title = "QUIT"
dialog_text = "Are you sure want to close?"
window.configure(background="white")
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

message = tk.Label(
    window,
    text="Face Recognition Based Attendance Management System",
    bg="Grey",
    fg="white",
    width=50,
    height=3,
    font=("times", 30, "italic bold underline"),
)
message.place(x=65, y=20)

# ER no
lbl1 = tk.Label(
    window,
    text="Enrollment No",
    width=10,
    height=2,
    fg="white",
    bg="Grey",
    font=("times", 15, "bold"),
)
lbl1.place(x=200, y=200)
txt1 = tk.Entry(window, width=17, bg="Grey", fg="white", font=("times", 27, "bold"))
txt1.place(x=400, y=204)
# name
lbl2 = tk.Label(
    window,
    text="Name",
    width=10,
    height=2,
    fg="white",
    bg="Grey",
    font=("times", 15, "bold"),
)
lbl2.place(x=200, y=275)
txt2 = tk.Entry(window, width=17, bg="Grey", fg="white", font=("times", 27, "bold"))
txt2.place(x=400, y=280)

lbl3 = tk.Label(
    window,
    text="Notification",
    width=10,
    height=2,
    fg="white",
    bg="Grey",
    font=("times", 15, "bold"),
)
lbl3.place(x=200, y=350)

message = tk.Label(
    window,
    text="",
    bg="Grey",
    fg="white",
    width=40,
    height=2,
    activebackground="black",
    font=("times", 15, "bold"),
)
message.place(x=400, y=350)


# to clear text box
def clear():
    txt1.delete(0, "end")
    res = ""
    message.configure(text=res)


def clear2():
    txt2.delete(0, "end")
    res = ""
    message.configure(text=res)


# to destroy screen
def del_sc1():
    sc1.destroy()


def del_sc2():
    sc2.destroy()


# error message for name and no
def err_screen():
    global sc1
    sc1 = tk.Tk()
    sc1.geometry("300x100")
    sc1.iconbitmap("AMS.ico")
    sc1.title("Warning!!")
    sc1.configure(background="snow")
    tk.Label(
        sc1,
        text="Enrollment & Name required!!!",
        fg="red",
        bg="white",
        font=("times", 16, " bold "),
    ).pack()
    tk.Button(
        sc1,
        text="OK",
        command=del_sc1,
        fg="black",
        bg="lawn green",
        width=9,
        height=1,
        activebackground="Red",
        font=("times", 15, " bold "),
    ).place(x=90, y=50)


# error message for subject
def err_screen1():
    global sc2
    sc2 = tk.Tk()
    sc2.geometry("300x100")
    sc2.iconbitmap("AMS.ico")
    sc2.title("Warning!!")
    sc2.configure(background="snow")
    tk.Label(
        sc2,
        text="Please enter your subject name!!!",
        fg="red",
        bg="white",
        font=("times", 16, " bold "),
    ).pack()
    tk.Button(
        sc2,
        text="OK",
        command=del_sc2,
        fg="black",
        bg="lawn green",
        width=9,
        height=1,
        activebackground="Red",
        font=("times", 15, " bold "),
    ).place(x=90, y=50)


def register_student():
    win = tk.Tk()
    win.iconbitmap("AMS.ico")
    win.title("LogIn")
    win.geometry("880x420")
    win.configure(background="snow")
    win.destroy()
    import csv
    import tkinter

    root = tkinter.Tk()
    root.title("Student Details")
    root.configure(background="snow")

    cs = "C:\\Users\\patel\\OneDrive\\Documents\\E\\FBAS\\StudentDetails\\studentdetails.csv"
    with open(cs, newline="") as file:
        reader = csv.reader(file)
        r = 0

        for col in reader:
            c = 0
            for row in col:
                # i've added some styling
                label = tkinter.Label(
                    root,
                    width=8,
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


def take_image():
    l1 = txt1.get()
    l2 = txt2.get()
    takeImage.TakeImage(l1, l2, haarcasecade_path, trainimage_path, message, err_screen)


# image
takeImg = tk.Button(
    window,
    text="Take Image",
    command=take_image,
    fg="white",
    bg="Grey",
    width=15,
    height=3,
    activebackground="Black",
    font=("times", 15, "bold"),
)


def train_image():
    trainImage.TrainImage(
        haarcasecade_path, trainimage_path, trainimagelabel_path, message
    )


takeImg.place(x=140, y=450)
trainImg = tk.Button(
    window,
    text="Train Image",
    command=train_image,
    fg="white",
    bg="Grey",
    width=15,
    height=3,
    activebackground="Black",
    font=("times", 15, "bold"),
)
trainImg.place(x=450, y=450)


def automatic_attedance():
    automaticAttedance.subjectChoose(err_screen1)


trackImg = tk.Button(
    window,
    text="Automatic Attendance",
    command=automatic_attedance,
    fg="white",
    bg="Grey",
    width=17,
    height=3,
    activebackground="Black",
    font=("times", 15, "bold"),
)
trackImg.place(x=750, y=450)


def view_attendance():
    show_attendance.subjectchoose()


trackImg = tk.Button(
    window,
    text="View Attendance",
    command=view_attendance,
    fg="white",
    bg="Grey",
    width=17,
    height=3,
    activebackground="Black",
    font=("times", 15, "bold"),
)
trackImg.place(x=240, y=550)

trackImg = tk.Button(
    window,
    text="Check Register Student",
    command=register_student,
    fg="white",
    bg="Grey",
    width=18,
    height=3,
    activebackground="Black",
    font=("times", 15, "bold"),
)
trackImg.place(x=580, y=550)


quitwindow = tk.Button(
    window,
    text="Quit",
    command=window.destroy,
    fg="white",
    bg="Grey",
    width=10,
    height=3,
    activebackground="Black",
    font=("times", 15, "bold"),
)
quitwindow.place(x=930, y=550)
