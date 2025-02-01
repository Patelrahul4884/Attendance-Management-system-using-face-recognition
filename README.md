
# Face based attendance system using python and openCV

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)                 
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/) 

### What steps you have to follow??
- Download or clone my Repository to your device
- type `pip install -r requirements.txt` in command prompt(this will install required package for project)
- Create a `TrainingImage` folder in a project folder.
- open `attendance.py` and `automaticAttendance.py`, change all the path accoriding to your system
- Run `attandance.py` file

### Project flow & explaination
- After you run the project you have to register your face so that system can identify you, so click on register new student
- After you click a small window will pop up in that you have to enter you ID and name and then click on `Take Image` button
- After clicking `Take Image` button A camera window will pop up and it will detect your Face and take upto 50 Images(you can change the number of Image it can take) and stored in the folder named `TrainingImage`. more you give the image to system, the better it will perform while recognising the face.
- Then you have to click on `Train Image` button, It will train the model and convert all the Image into numeric format so that computer can understand. we are training the image so that next time when we will show the same face to the computer it will easily identify the face.
- It will take some time(depends on you system).
- After training model click on `Automatic Attendance` ,you have to enter the subject name and then it can fill attendace by your face using our trained model.
- it will create `.csv` file for every subject you enter and seperate every `.csv` file accoriding the subject
- You can view the attendance after clicking `View Attendance` button. It will show record in tabular format.

### Screenshots

### Simple UI
<img src='https://github.com/Patelrahul4884/Attendance-Management-system-using-face-recognition/blob/master/Project%20Snap/1.PNG'>

### While taking Image
![Screenshot (103)](https://user-images.githubusercontent.com/26384517/86820502-c7f44500-c0a6-11ea-9530-6317ec2059d9.png)

## While taking Attendance
![Screenshot (91)](https://user-images.githubusercontent.com/26384517/86821090-9465ea80-c0a7-11ea-9680-777923663d0c.png)

## Attendance in tabular format 
<img src='https://github.com/Patelrahul4884/Attendance-Management-system-using-face-recognition/blob/master/Project%20Snap/7.PNG'>

## Just follow me and Star⭐ my repository
