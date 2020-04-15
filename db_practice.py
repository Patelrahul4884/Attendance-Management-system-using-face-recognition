<<<<<<< HEAD
from firebase import firebase
firebase = firebase.FirebaseApplication('https://face-attendance-211a7.firebaseio.com/', None)  
data =  { 'Name': 'rahul',  
          'RollNo': 1,  
          'Percentage': 76.02  
          }  
result = firebase.post('/face-attendance-211a7/studnet',data)  
print(result)  
=======
import mysql.connector

mydb=mysql.connector.connect(host='localhost',user='root',passwd='',database='face_recog_fill')
mycursor=mydb.cursor()


insert_data="INSERT INTO sub_attedance (ID,ENROLLMENT,NAME,DATE,TIME) VALUES (0, %s, %s, %s,%s)"
VALUES = (160450116033, "rahul", 20200303,11)
mydb.commit()
print(mycursor.rowcount, "record inserted.")
>>>>>>> parent of 57ca506... minor chnages
