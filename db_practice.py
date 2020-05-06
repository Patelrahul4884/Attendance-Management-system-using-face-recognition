from firebase import firebase
firebase = firebase.FirebaseApplication('https://face-attendance-211a7.firebaseio.com/', None)  
data =  { 'Name': 'rahul',  
          'RollNo': 1,  
          'Percentage': 76.02  
          }  
result = firebase.post('/face-attendance-211a7/studnet',data)  
print(result)  
