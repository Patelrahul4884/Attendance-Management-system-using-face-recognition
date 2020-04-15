import tkinter as tk
from tkinter import Message,Text
import os,cv2
import shutil
import csv
import numpy as np 
from PIL import ImageTk,Image
import pandas as pd 
import datetime
import time
import tkinter.ttk as tkk
import tkinter.font as font

window=tk.Tk()
window.title("Face recognizer")
window.geometry("1280x720")
dialog_title='QUIT'
dialog_text='Are you sure want to close?'
window.configure(background='white')
window.grid_rowconfigure(0,weight=1)
window.grid_columnconfigure(0,weight=1)
haarcascadePath='C:\\Users\\patel\\OneDrive\\Documents\\E\\FBAS\\haarcascade_frontalface_default.xml'

message=tk.Label(window,text="Face Recognition Based Attendance Management System",bg='Grey',fg='white',width=50,height=3,font=('times',30,'italic bold underline'))
message.place(x=65,y=20)
def testVal(inStr,acttyp):
    if acttyp == '1': #insert
        if not inStr.isdigit():
            return False
    return True
#ER no
lbl1=tk.Label(window,text="Enrollment No",width=10,height=2,fg='white',bg='Grey',font=('times',15,'bold'))
lbl1.place(x=200,y=200)
txt1=tk.Entry(window,width=17,bg='Grey',fg='white',font=('times',27,'bold'))
txt1.place(x=400,y=204)
#name
lbl2=tk.Label(window,text="Name",width=10,height=2,fg='white',bg='Grey',font=('times',15,'bold'))
lbl2.place(x=200,y=275)
txt2=tk.Entry(window,width=17,bg='Grey',fg='white',font=('times',27,'bold'))
txt2.place(x=400,y=280)

lbl3=tk.Label(window,text="Notification",width=10,height=2,fg='white',bg='Grey',font=('times',15,'bold'))
lbl3.place(x=200,y=350)

message=tk.Label(window,text="",bg='Grey',fg='white',width=40,height=2,activebackground='black',font=('times',15,'bold'))
message.place(x=400,y=350)

lbl4=tk.Label(window,text="Attendance",width=10,height=2,fg='white',bg='Grey',font=('times',15,'bold underline'))
lbl4.place(x=200,y=600)

message2=tk.Label(window,text="",bg='Grey',fg='white',activebackground='black',width=25,height=2,font=('times',15,'bold'))
message2.place(x=400,y=600)

#to clear text box
def clear():
    txt1.delete(0,'end')
    res=''
    message.configure(text=res)

def clear2():
    txt2.delete(0,'end')
    res=''
    message.configure(text=res)
def del_sc1():
    sc1.destroy()
def err_screen():
    global sc1
    sc1 = tk.Tk()
    sc1.geometry('300x100')
    sc1.iconbitmap('AMS.ico')
    sc1.title('Warning!!')
    sc1.configure(background='snow')
    tk.Label(sc1,text='Enrollment & Name required!!!',fg='red',bg='white',font=('times', 16, ' bold ')).pack()
    tk.Button(sc1,text='OK',command=del_sc1,fg="black"  ,bg="lawn green"  ,width=9  ,height=1, activebackground = "Red" ,font=('times', 15, ' bold ')).place(x=90,y= 50)

def del_sc2():
    sc2.destroy()
def err_screen1():
    global sc2
    sc2 = tk.Tk()
    sc2.geometry('300x100')
    sc2.iconbitmap('AMS.ico')
    sc2.title('Warning!!')
    sc2.configure(background='snow')
    tk.Label(sc2,text='Please enter your subject name!!!',fg='red',bg='white',font=('times', 16, ' bold ')).pack()
    tk.Button(sc2,text='OK',command=del_sc2,fg="black"  ,bg="lawn green"  ,width=9  ,height=1, activebackground = "Red" ,font=('times', 15, ' bold ')).place(x=90,y= 50)

#take Image of user
def TakeImage():
    l1=txt1.get()
    l2=txt2.get()
    if l1=='':
        err_screen()
    elif l2=='':
        err_screen()
    else:
        try:        
            cam=cv2.VideoCapture(0)
            detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            Enrollment=txt1.get()
            Name=txt2.get()
            sampleNum=0
            while(True):
                ret,img=cam.read()
                gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                faces=detector.detectMultiScale(gray,1.3,5)
                for(x,y,w,h) in faces:
                    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                    sampleNum=sampleNum+1
                    cv2.imwrite("TrainingImage\ "+Name +"_"+Enrollment +'_' +str(sampleNum)+".jpg",gray[y:y+h,x:x+w])
                    cv2.imshow('Frame',img)
                if cv2.waitKey(1) & 0xFF== ord('q'):
                    break
                elif sampleNum>40:
                    break
            cam.release()
            cv2.destroyAllWindows()
            row = [Enrollment, Name]
            with open('StudentDetails\studentdetails.csv','a+') as csvFile:
                writer=csv.writer(csvFile,delimiter=',')
                writer.writerow(row)
                csvFile.close()
            res = "Images Saved for Enrollment : " + Enrollment + " Name : " + Name
            message.configure(text=res)
        except FileExistsError as f:
            f='Student Data already exists'
            message.configure(text=f)
            
#Train Image
def TrainImage():
    recognizer=cv2.face.LBPHFaceRecognizer_create()
    detector=cv2.CascadeClassifier(haarcascadePath)
    faces,Id=getImagesAndLables("TrainingImage")
    recognizer.train(faces,np.array(Id))
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res="Image Trained" #+",".join(str(f) for f in Id)
    message.configure(text=res)
def getImagesAndLables(path):
    imagePath=[os.path.join(path,f) for f in os.listdir(path)]
    faces=[]
    Ids=[]
    for imagePath in imagePath:
        pilImage=Image.open(imagePath).convert('L')
        imageNp=np.array(pilImage,'uint8')
        Id=int(os.path.split(imagePath)[-1].split("_")[1])
        faces.append(imageNp)
        Ids.append(Id)
    return faces,Ids


#for choose subject and fill attendance
def subjectChoose():
    def FillAttendance():
        sub=tx.get()
        now=time.time()
        future=now+20
        if now<future:
            if sub=='':
                err_screen1()
            else:
                recognizer=cv2.face.LBPHFaceRecognizer_create()
                try:
                    recognizer.read("TrainingImageLabel\Trainner.yml")
                except:
                    e="Model not found,please train model"
                    Notifica.configure(text=e,bg='Grey',fg='white',width=33,font=('times',15,'bold'))
                    Notifica.place(x=20,y=250)
                facecasCade=cv2.CascadeClassifier(haarcascadePath)
                df=pd.read_csv("StudentDetails\studentdetails.csv")
                cam=cv2.VideoCapture(0)
                font=cv2.FONT_HERSHEY_SIMPLEX
                col_names=['Enrollment', 'Name']
                attendance=pd.DataFrame(columns=col_names)
                while True:
                    ret,im=cam.read()
                    gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
                    faces=facecasCade.detectMultiScale(gray,1.2,5)
                    for(x,y,w,h) in faces:
                        global Id

                        Id,conf=recognizer.predict(gray[y:y+h,x:x+w])
                        if(conf<60):
                            print(conf)
                            global Subject 
                            global aa
                            global date
                            global timeStamp
                            Subject=tx.get()
                            ts=time.time()
                            date=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                            timeStamp=datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                            aa=df.loc[df['Enrollment']==Id]['Name'].values

                            global tt
                            tt=str(Id)+"-"+aa
                            #En='1604501160'+str(Id)
                            attendance.loc[len(attendance)]=[Id,aa]
                            cv2.rectangle(im,(x,y),(x+w,y+h),(0,260,0),7)
                            cv2.putText(im,str(tt),(x+h,y),font,1,(255,255,0,),4)
                        else:
                            Id='Unknown'
                            tt=str(Id)
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                            cv2.putText(im, str(tt), (x + h, y), font, 1, (0, 25, 255), 4)       
                    if time.time()>future:
                        break

                    
                    attendance=attendance.drop_duplicates(['Enrollment'],keep='first')
                    cv2.imshow('Filling Attendance...',im)
                    key=cv2.waitKey(30)&0xFF
                    if key==27:
                        break
                ts = time.time()
                attendance[date]="P"
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                Hour, Minute, Second = timeStamp.split(":")
                fileName = "Attendance/" + Subject + "_" + date + "_" + Hour + "-" + Minute + "-" + Second + ".csv"
                attendance = attendance.drop_duplicates(['Enrollment'], keep='first')
                print(attendance)
                attendance.to_csv(fileName, index=False)

                m='Attendance Filled Successfully'
                Notifica.configure(text=m,bg='Grey',fg='white',width=33,font=('times',15,'bold'))
                Notifica.place(x=20,y=250)

                cam.release()
                cv2.destroyAllWindows()


                import csv
                import tkinter
                root = tkinter.Tk()
                root.title("Attendance of " + Subject)
                root.configure(background='snow')
                cs = 'C:\\Users\\patel\\OneDrive\\Documents\\E\\FBAS\\' + fileName
                with open(cs, newline="") as file:
                    reader = csv.reader(file)
                    r = 0

                    for col in reader:
                        c = 0
                        for row in col:
            
                            label = tkinter.Label(root, width=10, height=1, fg="black", font=('times', 15, ' bold '),bg="lawn green", text=row, relief=tkinter.RIDGE)
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                root.mainloop()
                print(attendance)


                
 ###windo is frame for subject chooser
    windo = tk.Tk()
    windo.iconbitmap('AMS.ico')
    windo.title("Enter subject name...")
    windo.geometry('580x320')
    windo.configure(background='snow')
    Notifica = tk.Label(windo, text="Attendance filled Successfully", bg="Green", fg="white", width=33,
                            height=2, font=('times', 15, 'bold'))

    def Attf():
        import subprocess
        subprocess.Popen(r'explorer \\select,"C:\\Users\\patel\\OneDrive\Documents\\E\\FBAS\\"')

    attf = tk.Button(windo,  text="Check Sheets",command=Attf,fg="black"  ,bg="lawn green"  ,width=12  ,height=1 ,activebackground = "Red" ,font=('times', 14, ' bold '))
    attf.place(x=430, y=255)

    sub = tk.Label(windo, text="Enter Subject", width=15, height=2, fg="white", bg="blue2", font=('times', 15, ' bold '))
    sub.place(x=30, y=100)

    tx = tk.Entry(windo, width=20, bg="yellow", fg="red", font=('times', 23, ' bold '))
    tx.place(x=250, y=105)

    fill_a = tk.Button(windo, text="Fill Attendance", fg="white",command=FillAttendance, bg="deep pink", width=20, height=2,
                       activebackground="Red", font=('times', 15, ' bold '))
    fill_a.place(x=250, y=160)
    windo.mainloop()


def admin_panel():
    win = tk.Tk()
    win.iconbitmap('AMS.ico')
    win.title("LogIn")
    win.geometry('880x420')
    win.configure(background='snow')

    def log_in():
        username = un_entr.get()
        password = pw_entr.get()

        if username == 'unreal' :
            if password == 'unreal':
                win.destroy()
                import csv
                import tkinter
                root = tkinter.Tk()
                root.title("Student Details")
                root.configure(background='snow')

                cs = 'C:\\Users\\patel\\OneDrive\\Documents\\E\\FBAS\\StudentDetails\\studentdetails.csv'
                with open(cs, newline="") as file:
                    reader = csv.reader(file)
                    r = 0

                    for col in reader:
                        c = 0
                        for row in col:
                            # i've added some styling
                            label = tkinter.Label(root, width=8, height=1, fg="black", font=('times', 15, ' bold '),
                                                  bg="lawn green", text=row, relief=tkinter.RIDGE)
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                root.mainloop()
            else:
                valid = 'Incorrect ID or Password'
                message.configure(text=valid, bg="red", fg="black", width=38, font=('times', 19, 'bold'))
                message.place(x=120, y=350)

        else:
            valid ='Incorrect ID or Password'
            message.configure(text=valid, bg="red", fg="black", width=38, font=('times', 19, 'bold'))
            message.place(x=120, y=350)


#clear Button
clearbutton=tk.Button(window,text="Clear",command=clear,fg='white',bg='Grey',width=10,activebackground='black',font=('times',17,'bold'))
clearbutton.place(x=750,y=204)
clearbutton=tk.Button(window,text="Clear",command=clear2,fg='white',bg='Grey',width=10,activebackground='black',font=('times',17,'bold'))
clearbutton.place(x=750,y=280)

#image
takeImg=tk.Button(window,text="Take Image",command=TakeImage,fg='white',bg='Grey',width=15,height=3,activebackground='Black',font=('times',15,'bold'))
takeImg.place(x=40,y=450)
trainImg=tk.Button(window,text="Train Image",command=TrainImage,fg='white',bg='Grey',width=15,height=3,activebackground='Black',font=('times',15,'bold'))
trainImg.place(x=300,y=450)
trackImg=tk.Button(window,text="Automatic Attendance",command=subjectChoose,fg='white',bg='Grey',width=15,height=3,activebackground='Black',font=('times',15,'bold'))
trackImg.place(x=550,y=450)

trackImg=tk.Button(window,text="Check Register Student",command=admin_panel,fg='white',bg='Grey',width=15,height=3,activebackground='Black',font=('times',15,'bold'))
trackImg.place(x=780,y=450)


quitwindow=tk.Button(window,text="Quit",command=window.destroy,fg='white',bg='Grey',width=10,height=3,activebackground='Black',font=('times',15,'bold'))
quitwindow.place(x=1050,y=450)
