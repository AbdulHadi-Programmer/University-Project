# 🎓 StudyMate

**StudyMate** is a student productivity web application built with **Django**.  
It helps students stay organized by managing subjects, tasks, learning items, and class timetables — all in one place.

---

## 🚀 Features

- **User Authentication**  
  Secure login, registration, and profile management.

- **Dashboard**  
  Overview of enrolled subjects with quick navigation.

- **Task Management**  
  Create, update, and delete academic tasks with deadlines.

- **Learning Items**  
  Add and manage study resources linked to subjects.

- **Class Timetable**  
  Responsive timetable view with the current day highlighted.

---

## 🛠️ Tech Stack

- **Backend**: Django (Python)  
- **Frontend**: Bootstrap 5, FontAwesome Icons  
- **Database**: SQLite (default, easily switchable to PostgreSQL/MySQL)  

---

## 📂 Project Structure

```
StudyMate/
│── academy_tracker/   # Main Django project
│── accounts/          # User authentication and profiles
│── tasks/             # Task CRUD functionality
│── subjects/          # Subjects and learning items
│── templates/         # HTML templates (Bootstrap-based)
│── static/            # Static assets (CSS, JS, icons)
│── db.sqlite3         # Default SQLite database
```

---

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/StudyMate.git
   cd StudyMate
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/Mac
   venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

5. **Run the development server**
   ```bash
   python manage.py runserver
   ```

6. **Access the app**  
   Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## 📧 Future Enhancements

- Email reminders for pending and due tasks.  
- Password reset & email verification.  
- Profile pictures and extended student settings.  
- Improved security and notifications.  

---

## 📜 License

This project is licensed under the **MIT License**.  
Feel free to use and modify for your own learning or projects.