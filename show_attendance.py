import pandas as pd
from glob import glob
import os
import tkinter
import csv
import tkinter as tk


def subjectchoose():
    def calculate_attendance():
        Subject = tx.get()
        os.chdir(
            f"C:\\Users\\patel\\OneDrive\\Documents\\E\\FBAS\\Attendance\\{Subject}"
        )
        filenames = glob(
            f"C:\\Users\\patel\\OneDrive\\Documents\\E\\FBAS\\Attendance\\{Subject}\\{Subject}*.csv"
        )
        df = [pd.read_csv(f) for f in filenames]
        newdf = df[0]
        for i in range(1, len(df)):
            newdf = newdf.merge(df[i], how="outer")
        newdf.fillna(0, inplace=True)
        newdf["Attendance"] = 0
        for i in range(len(newdf)):
            newdf["Attendance"].iloc[i] = newdf.iloc[i, 2:-1].mean() * 100
        newdf.to_csv("attendance.csv", index=False)

        root = tkinter.Tk()
        root.title("Attendance of python ")
        root.configure(background="snow")
        cs = f"C:\\Users\\patel\\OneDrive\\Documents\\E\\FBAS\\Attendance\\{Subject}\\attendance.csv"
        with open(cs) as file:
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
        print(newdf)

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
        text="View Attendance",
        fg="white",
        command=calculate_attendance,
        bg="grey",
        width=20,
        height=2,
        activebackground="Red",
        font=("times", 15, " bold "),
    )
    fill_a.place(x=250, y=160)
    windo.mainloop()
