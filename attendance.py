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

# from firebase import firebase
# firebase = firebase.FirebaseApplication('https://face-attendance-211a7.firebaseio.com/', None)
window = tk.Tk()
window.title("Face recognizer")
window.geometry("1024x768")
dialog_title = "QUIT"
dialog_text = "Are you sure want to close?"
window.configure(background="white")
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
haarcascadePath = "C:\\Users\\patel\\OneDrive\\Documents\\E\\FBAS\\haarcascade_frontalface_default.xml"

####GUI for manually fill attendance


def manually_fill():
    global sb
    sb = tk.Tk()
    sb.iconbitmap("AMS.ico")
    sb.title("Enter subject name...")
    sb.geometry("580x320")
    sb.configure(background="snow")

    def err_screen_for_subject():
        def ec_delete():
            ec.destroy()

        global ec
        ec = tk.Tk()
        ec.geometry("300x100")
        ec.iconbitmap("AMS.ico")
        ec.title("Warning!!")
        ec.configure(background="snow")
        tk.Label(
            ec,
            text="Please enter your subject name!!!",
            fg="red",
            bg="white",
            font=("times", 16, " bold "),
        ).pack()
        tk.Button(
            ec,
            text="OK",
            command=ec_delete,
            fg="black",
            bg="lawn green",
            width=9,
            height=1,
            activebackground="Red",
            font=("times", 15, " bold "),
        ).place(x=90, y=50)

    def fill_attendance():
        ts = time.time()
        Date = datetime.datetime.fromtimestamp(ts).strftime("%Y_%m_%d")
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
        Time = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
        Hour, Minute, Second = timeStamp.split(":")
        ####Creatting csv of attendance

        ##Create table for Attendance
        date_for_DB = datetime.datetime.fromtimestamp(ts).strftime("%Y_%m_%d")
        global subb
        subb = SUB_ENTRY.get()
        DB_table_name = str(
            subb + "_" + Date + "_Time_" + Hour + "_" + Minute + "_" + Second
        )

        import pymysql.connections

        ###Connect to the database
        try:
            global cursor
            connection = pymysql.connect(
                host="localhost",
                user="root",
                password="",
                db="manually_fill_attendance",
            )
            cursor = connection.cursor()
        except Exception as e:
            print(e)

        sql = (
            "CREATE TABLE "
            + DB_table_name
            + """
                        (ID INT NOT NULL AUTO_INCREMENT,
                         ENROLLMENT varchar(100) NOT NULL,
                         NAME VARCHAR(50) NOT NULL,
                         DATE VARCHAR(20) NOT NULL,
                         TIME VARCHAR(20) NOT NULL,
                             PRIMARY KEY (ID)
                             );
                        """
        )

        try:
            cursor.execute(sql)  ##for create a table
            connection.commit()
        except Exception as ex:
            print(ex)  #

        if subb == "":
            err_screen_for_subject()
        else:
            sb.destroy()
            MFW = tk.Tk()
            MFW.iconbitmap("AMS.ico")
            MFW.title("Manually attendance of " + str(subb))
            MFW.geometry("880x470")
            MFW.configure(background="snow")

            def del_errsc2():
                errsc2.destroy()

            def err_screen1():
                global errsc2
                errsc2 = tk.Tk()
                errsc2.geometry("330x100")
                errsc2.iconbitmap("AMS.ico")
                errsc2.title("Warning!!")
                errsc2.configure(background="snow")
                tk.Label(
                    errsc2,
                    text="Please enter Student & Enrollment!!!",
                    fg="red",
                    bg="white",
                    font=("times", 16, " bold "),
                ).pack()
                tk.Button(
                    errsc2,
                    text="OK",
                    command=del_errsc2,
                    fg="black",
                    bg="lawn green",
                    width=9,
                    height=1,
                    activebackground="Red",
                    font=("times", 15, " bold "),
                ).place(x=90, y=50)

            def testVal(inStr, acttyp):
                if acttyp == "1":  # insert
                    if not inStr.isdigit():
                        return False
                return True

            ENR = tk.Label(
                MFW,
                text="Enter Enrollment",
                width=15,
                height=2,
                fg="white",
                bg="blue2",
                font=("times", 15, " bold "),
            )
            ENR.place(x=30, y=100)

            STU_NAME = tk.Label(
                MFW,
                text="Enter Student name",
                width=15,
                height=2,
                fg="white",
                bg="blue2",
                font=("times", 15, " bold "),
            )
            STU_NAME.place(x=30, y=200)

            global ENR_ENTRY
            ENR_ENTRY = tk.Entry(
                MFW,
                width=20,
                validate="key",
                bg="yellow",
                fg="red",
                font=("times", 23, " bold "),
            )
            ENR_ENTRY["validatecommand"] = (ENR_ENTRY.register(testVal), "%P", "%d")
            ENR_ENTRY.place(x=290, y=105)

            def remove_enr():
                ENR_ENTRY.delete(first=0, last=22)

            STUDENT_ENTRY = tk.Entry(
                MFW, width=20, bg="yellow", fg="red", font=("times", 23, " bold ")
            )
            STUDENT_ENTRY.place(x=290, y=205)

            def remove_student():
                STUDENT_ENTRY.delete(first=0, last=22)

            ####get important variable
            def enter_data_DB():
                ENROLLMENT = ENR_ENTRY.get()
                STUDENT = STUDENT_ENTRY.get()
                if ENROLLMENT == "":
                    err_screen1()
                elif STUDENT == "":
                    err_screen1()
                else:
                    time = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
                    Hour, Minute, Second = time.split(":")
                    Insert_data = (
                        "INSERT INTO "
                        + DB_table_name
                        + " (ID,ENROLLMENT,NAME,DATE,TIME) VALUES (0, %s, %s, %s,%s)"
                    )
                    VALUES = (str(ENROLLMENT), str(STUDENT), str(Date), str(time))
                    try:
                        cursor.execute(Insert_data, VALUES)
                    except Exception as e:
                        print(e)
                    ENR_ENTRY.delete(first=0, last=22)
                    STUDENT_ENTRY.delete(first=0, last=22)

            def create_csv():
                import csv

                cursor.execute("select * from " + DB_table_name + ";")
                csv_name = (
                    "C:\\Users\\patel\\OneDrive\\Documents\\E\\FBAS\\Attendance(Manually)\\"
                    + DB_table_name
                    + ".csv"
                )
                with open(csv_name, "w") as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow(
                        [i[0] for i in cursor.description]
                    )  # write headers
                    csv_writer.writerows(cursor)
                    O = "CSV created Successfully"
                    Notifi.configure(
                        text=O,
                        bg="Green",
                        fg="white",
                        width=33,
                        font=("times", 19, "bold"),
                    )
                    Notifi.place(x=180, y=380)
                import csv
                import tkinter

                root = tkinter.Tk()
                root.title("Attendance of " + subb)
                root.configure(background="snow")
                with open(csv_name, newline="") as file:
                    reader = csv.reader(file)
                    r = 0

                    for col in reader:
                        c = 0
                        for row in col:
                            # i've added some styling
                            label = tkinter.Label(
                                root,
                                width=13,
                                height=1,
                                fg="black",
                                font=("times", 13, " bold "),
                                bg="lawn green",
                                text=row,
                                relief=tkinter.RIDGE,
                            )
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                root.mainloop()

            Notifi = tk.Label(
                MFW,
                text="CSV created Successfully",
                bg="Green",
                fg="white",
                width=33,
                height=2,
                font=("times", 19, "bold"),
            )

            c1ear_enroll = tk.Button(
                MFW,
                text="Clear",
                command=remove_enr,
                fg="black",
                bg="deep pink",
                width=10,
                height=1,
                activebackground="Red",
                font=("times", 15, " bold "),
            )
            c1ear_enroll.place(x=690, y=100)

            c1ear_student = tk.Button(
                MFW,
                text="Clear",
                command=remove_student,
                fg="black",
                bg="deep pink",
                width=10,
                height=1,
                activebackground="Red",
                font=("times", 15, " bold "),
            )
            c1ear_student.place(x=690, y=200)

            DATA_SUB = tk.Button(
                MFW,
                text="Enter Data",
                command=enter_data_DB,
                fg="black",
                bg="lime green",
                width=20,
                height=2,
                activebackground="Red",
                font=("times", 15, " bold "),
            )
            DATA_SUB.place(x=170, y=300)

            MAKE_CSV = tk.Button(
                MFW,
                text="Convert to CSV",
                command=create_csv,
                fg="black",
                bg="red",
                width=20,
                height=2,
                activebackground="Red",
                font=("times", 15, " bold "),
            )
            MAKE_CSV.place(x=570, y=300)
            # TODO remove check sheet
            def attf():
                import subprocess

                subprocess.Popen(
                    r'explorer /select,"C:/Users/patel/OneDrive/Documents/E/FBAS/Attendance(Manually)"'
                )

            attf = tk.Button(
                MFW,
                text="Check Sheets",
                command=attf,
                fg="black",
                bg="lawn green",
                width=12,
                height=1,
                activebackground="Red",
                font=("times", 14, " bold "),
            )
            attf.place(x=730, y=410)

            MFW.mainloop()

    SUB = tk.Label(
        sb,
        text="Enter Subject",
        width=15,
        height=2,
        fg="white",
        bg="blue2",
        font=("times", 15, " bold "),
    )
    SUB.place(x=30, y=100)

    global SUB_ENTRY

    SUB_ENTRY = tk.Entry(
        sb, width=20, bg="yellow", fg="red", font=("times", 23, " bold ")
    )
    SUB_ENTRY.place(x=250, y=105)

    fill_manual_attendance = tk.Button(
        sb,
        text="Fill Attendance",
        command=fill_attendance,
        fg="white",
        bg="deep pink",
        width=20,
        height=2,
        activebackground="Red",
        font=("times", 15, " bold "),
    )
    fill_manual_attendance.place(x=250, y=160)
    sb.mainloop()


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


# take Image of user
def TakeImage():
    l1 = txt1.get()
    l2 = txt2.get()
    if l1 == "":
        err_screen()
    elif l2 == "":
        err_screen()
    else:
        try:
            cam = cv2.VideoCapture(0)
            detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
            Enrollment = l1
            Name = l2
            sampleNum = 0
            while True:
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    sampleNum = sampleNum + 1
                    cv2.imwrite(
                        f"TrainingImage\ "
                        + Name
                        + "_"
                        + Enrollment
                        + "_"
                        + str(sampleNum)
                        + ".jpg",
                        gray[y : y + h, x : x + w],
                    )
                    cv2.imshow("Frame", img)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
                elif sampleNum > 70:
                    break
            cam.release()
            cv2.destroyAllWindows()
            row = [Enrollment, Name]
            with open("StudentDetails\studentdetails.csv", "a+") as csvFile:
                writer = csv.writer(csvFile, delimiter=",")
                writer.writerow(row)
                csvFile.close()
            res = "Images Saved for Enrollment : " + Enrollment + " Name : " + Name
            message.configure(text=res)
        except FileExistsError as F:
            f = "Student Data already exists"
            message.configure(text=f)


# Train Image
def TrainImage():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier(haarcascadePath)
    faces, Id = getImagesAndLables("TrainingImage")
    recognizer.train(faces, np.array(Id))
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res = "Image Trained"  # +",".join(str(f) for f in Id)
    message.configure(text=res)


def getImagesAndLables(path):
    imagePath = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    Ids = []
    for imagePath in imagePath:
        pilImage = Image.open(imagePath).convert("L")
        imageNp = np.array(pilImage, "uint8")
        Id = int(os.path.split(imagePath)[-1].split("_")[1])
        faces.append(imageNp)
        Ids.append(Id)
    return faces, Ids


"""def TrainImage():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    global detector
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    try:
        global faces,Id
        faces, Id = getImagesAndLabels("TrainingImage")
    except Exception as e:
        l='please make "TrainingImage" folder & put Images'
        message.configure(text=l)

    recognizer.train(faces, np.array(Id))
    try:
        recognizer.save("TrainingImageLabel\Trainner.yml")
    except Exception as e:
        q='Please make "TrainingImageLabel" folder'
        message.configure(text=q)

    res = "Model Trained" # +",".join(str(f) for f in Id)
    message.configure(text=res)

def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empth face list
    faceSamples = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image

        Id = int(os.path.split(imagePath)[-1].split("_")[1])
        # extract the face from the training image sample
        faces = detector.detectMultiScale(imageNp)
        # If a face is there then append that in the list as well as Id of it
        for (x, y, w, h) in faces:
            faceSamples.append(imageNp[y:y + h, x:x + w])
            Ids.append(Id)
    return faceSamples, Ids"""

# for choose subject and fill attendance
def subjectChoose():
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
                    recognizer.read("TrainingImageLabel\Trainner.yml")
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
                facecasCade = cv2.CascadeClassifier(haarcascadePath)
                df = pd.read_csv("StudentDetails\studentdetails.csv")
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
                fileName = (
                    "Attendance/"
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
                cs = "C:\\Users\\patel\\OneDrive\\Documents\\E\\FBAS\\" + fileName
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
    windo.iconbitmap("AMS.ico")
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


def admin_panel():
    win = tk.Tk()
    win.iconbitmap("AMS.ico")
    win.title("LogIn")
    win.geometry("880x420")
    win.configure(background="snow")

    def log_in():
        username = un_entr.get()
        password = pw_entr.get()

        if username == "unreal":
            if password == "unreal":
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
            else:
                valid = "Incorrect ID or Password"
                message.configure(
                    text=valid,
                    bg="red",
                    fg="black",
                    width=38,
                    font=("times", 19, "bold"),
                )
                message.place(x=120, y=350)

        else:
            valid = "Incorrect ID or Password"
            message.configure(
                text=valid, bg="red", fg="black", width=38, font=("times", 19, "bold")
            )
            message.place(x=120, y=350)

    Nt = tk.Label(
        win,
        text="Attendance filled Successfully",
        bg="Green",
        fg="white",
        width=40,
        height=2,
        font=("times", 19, "bold"),
    )
    # Nt.place(x=120, y=350)

    un = tk.Label(
        win,
        text="Enter username",
        width=15,
        height=2,
        fg="white",
        bg="blue2",
        font=("times", 15, " bold "),
    )
    un.place(x=30, y=50)

    pw = tk.Label(
        win,
        text="Enter password",
        width=15,
        height=2,
        fg="white",
        bg="blue2",
        font=("times", 15, " bold "),
    )
    pw.place(x=30, y=150)

    def c00():
        un_entr.delete(first=0, last=22)

    un_entr = tk.Entry(
        win, width=20, bg="yellow", fg="red", font=("times", 23, " bold ")
    )
    un_entr.place(x=290, y=55)

    def c11():
        pw_entr.delete(first=0, last=22)

    pw_entr = tk.Entry(
        win, width=20, show="*", bg="yellow", fg="red", font=("times", 23, " bold ")
    )
    pw_entr.place(x=290, y=155)

    c0 = tk.Button(
        win,
        text="Clear",
        command=c00,
        fg="black",
        bg="deep pink",
        width=10,
        height=1,
        activebackground="Red",
        font=("times", 15, " bold "),
    )
    c0.place(x=690, y=55)

    c1 = tk.Button(
        win,
        text="Clear",
        command=c11,
        fg="white",
        bg="grey",
        width=10,
        height=1,
        activebackground="Red",
        font=("times", 15, " bold "),
    )
    c1.place(x=690, y=155)

    Login = tk.Button(
        win,
        text="LogIn",
        fg="black",
        bg="grey",
        width=20,
        height=2,
        activebackground="Red",
        command=log_in,
        font=("times", 15, " bold "),
    )
    Login.place(x=290, y=250)
    win.mainloop()


# clear Button
clearbutton = tk.Button(
    window,
    text="Clear",
    command=clear,
    fg="white",
    bg="Grey",
    width=10,
    activebackground="black",
    font=("times", 17, "bold"),
)
clearbutton.place(x=750, y=204)
clearbutton = tk.Button(
    window,
    text="Clear",
    command=clear2,
    fg="white",
    bg="Grey",
    width=10,
    activebackground="black",
    font=("times", 17, "bold"),
)
clearbutton.place(x=750, y=280)

# image
takeImg = tk.Button(
    window,
    text="Take Image",
    command=TakeImage,
    fg="white",
    bg="Grey",
    width=15,
    height=3,
    activebackground="Black",
    font=("times", 15, "bold"),
)
takeImg.place(x=140, y=450)
trainImg = tk.Button(
    window,
    text="Train Image",
    command=TrainImage,
    fg="white",
    bg="Grey",
    width=15,
    height=3,
    activebackground="Black",
    font=("times", 15, "bold"),
)
trainImg.place(x=450, y=450)
trackImg = tk.Button(
    window,
    text="Automatic Attendance",
    command=subjectChoose,
    fg="white",
    bg="Grey",
    width=17,
    height=3,
    activebackground="Black",
    font=("times", 15, "bold"),
)
trackImg.place(x=750, y=450)

trackImg = tk.Button(
    window,
    text="Check Register Student",
    command=admin_panel,
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

manual_attendance = tk.Button(
    window,
    text="Manually Fill Attendance",
    command=manually_fill,
    fg="white",
    bg="grey",
    width=20,
    height=3,
    activebackground="Red",
    font=("times", 15, " bold "),
)
manual_attendance.place(x=240, y=550)
