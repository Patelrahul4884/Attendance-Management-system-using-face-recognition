# Attendance Management System Using Face Recognition

A **Python-based attendance management system** using OpenCV and face recognition.  
This system allows you to register students by capturing face images, train a face recognition model, and automatically take and view attendance.

---

## 📌 Features
- Register new students with face images.
- Train face recognition model using Local Binary Patterns Histograms (LBPH).
- Take attendance automatically via webcam.
- View attendance logs.
- Text-to-speech notifications for better accessibility.

---

## 📂 Project Structure
Attendance-Management-system-using-face-recognition/
│
├── Attendance.py # Main GUI application
├── requirements.txt # Required Python packages
├── takeImage.py # Module to capture student face images
├── trainImage.py # Module to train face recognition model
├── automaticAttendance.py # Module for automated attendance capture
├── show_attendance.py # Module to view attendance logs
├── StudentDetails/ # Folder containing student details CSV
├── TrainingImage/ # Folder containing captured images
├── TrainingImageLabel/ # Folder containing trained model
├── UI_Image/ # Folder containing UI icons/images
└── README.md # Project documentation


---

## ⚙️ Requirements
- Python 3.8+
- OpenCV
- NumPy
- Pandas
- Pillow
- pyttsx3

---

## 📦 Installation
1. Clone the repository:
```bash
git clone https://github.com/<your-username>/Attendance-Management-system-using-face-recognition.git
cd Attendance-Management-system-using-face-recognition

Install dependencies:

pip install -r requirements.txt

🚀 How to Run

Run the main program:

python Attendance.py

📄 License

This project is licensed under the MIT License — see the LICENSE
 file for details.

💡 Contributing

Contributions are welcome!
If you find any bugs or want to add features, please open an issue or submit a pull request.

👤 Author

Mohd Mudabbir Arafat
Email: mudabbir.arafat@example.com

GitHub: https://github.com/Mudabbirarafat


---

