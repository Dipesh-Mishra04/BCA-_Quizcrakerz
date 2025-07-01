# 🧠 QuizzCrakerz

**QuizzCrakerz** is an educational web application built using Flask and MongoDB that allows users to take quizzes, view results, and explore various features like team info, services, and more. Designed with a clean UI using HTML, CSS, and Bootstrap, the app provides a smooth user experience for both students and admins.


## 🌐 Live Demo
https://bca-quizcrakerz.onrender.com

---

## 📌 Features

- ✅ Admin and User login system
- 🧠 Subject-wise quizzes
- 📊 Auto-evaluated results with score summary
- 📁 Responsive Dashboard
- 👥 Team and About Us pages
- 📞 Contact and Services info pages
- 🎨 Responsive and clean UI with Bootstrap

---

## 🛠️ Technologies Used

| Layer       | Tech Stack            |
|-------------|------------------------|
| Backend     | Python (Flask)         |
| Frontend    | HTML, CSS, Bootstrap   |
| Database    | MongoDB (via Flask-PyMongo) |
| Hosting     | Render                 |

---

## 🗂️ Folder Structure
quizzcrakerz/
├── backend/
│ ├── app.py
│ ├── config.py
│ ├── requirements.txt
│ ├── static/
│ │ ├── styling.css
│ │ ├── logo.jpg, dipesh.jpg, etc.
│ └── templates/
│ ├── index.html, quiz.html, result.html, etc.
├── render.yaml
└── README.md

---

## 🧪 Run Locally

### 🔧 Prerequisites

- Python 3.10+ installed
- Git installed
- MongoDB URI (e.g. from MongoDB Atlas)

### 🚀 Steps

#Clone the repository
git clone https://github.com/Dipesh-Mishra04/BCA-_Quizcrakerz.git
cd BCA-_Quizcrakerz/backend

# Create virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables (create .env or use export/set)
OPENAI_API_KEY=your_openai_key
MONGO_URI=your_mongo_uri

# Run the app
python app.py

.

🙋‍♂️ Author
Created with 💻 by Dipesh Mishra and team
📧 Contact: mishragdipesh@gmail.com

