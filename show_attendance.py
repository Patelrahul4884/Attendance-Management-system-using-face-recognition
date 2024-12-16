import pandas as pd
from glob import glob
import os
import tkinter
import csv
import tkinter as tk
from tkinter import *

def subjectchoose(text_to_speech):
    def calculate_attendance():
        Subject = tx.get()
        if Subject == "":
            t = 'Please enter the subject name.'
            text_to_speech(t)
        else:
            # Ensure the attendance directory exists
            attendance_dir = os.path.join("Attendance", Subject)
            if not os.path.exists(attendance_dir):
                t = f"The folder for subject '{Subject}' does not exist."
                text_to_speech(t)
                return

            os.chdir(attendance_dir)

            # Look for CSV files related to the subject
            filenames = glob(f"{Subject}*.csv")

            # Check if there are CSV files
            if not filenames:
                t = f"No attendance files found for the subject {Subject}."
                text_to_speech(t)
                return

            # Read all CSV files and merge them
            df = [pd.read_csv(f) for f in filenames]
            newdf = df[0]
            for i in range(1, len(df)):
                newdf = newdf.merge(df[i], how="outer")
            newdf.fillna(0, inplace=True)

            # Initialize the Attendance column as an empty string column
            newdf["Attendance"] = ""

            # Calculate attendance as percentage
            for i in range(len(newdf)):
                newdf.loc[i, "Attendance"] = f"{int(round(newdf.iloc[i, 2:-1].mean() * 100))}%"

            # Save the consolidated attendance to a new CSV
            newdf.to_csv("attendance.csv", index=False)

            # Display the attendance in a Tkinter window
            root = tkinter.Tk()
            root.title(f"Attendance of {Subject}")
            root.configure(background="black")

            # Ensure the file path is correctly formed
            attendance_file = os.path.join("E:\Attendance3\Attendance-Management-system-using-face-recognition\Attendance", Subject, "attendance.csv")
            
            # Print the file path to debug
            print(f"Looking for file at: {attendance_file}")

            # Check if file exists before attempting to open
            if not os.path.exists(attendance_file):
                t = f"The file for subject '{Subject}' does not exist."
                text_to_speech(t)
                return

            with open(attendance_file) as file:
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
            print(newdf)

    subject = Tk()
    subject.title("Subject...")
    subject.geometry("580x320")
    subject.resizable(0, 0)
    subject.configure(background="black")
    
    titl = tk.Label(subject, bg="black", relief=RIDGE, bd=10, font=("arial", 30))
    titl.pack(fill=X)

    titl = tk.Label(
        subject,
        text="Which Subject of Attendance?",
        bg="black",
        fg="green",
        font=("arial", 25),
    )
    titl.place(x=100, y=12)

    def Attf():
        sub = tx.get()
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            subject_dir = os.path.join("Attendance", sub)
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
        text="View Attendance",
        command=calculate_attendance,
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
