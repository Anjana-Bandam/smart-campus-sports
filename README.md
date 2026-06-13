# 🏆 Smart Campus Sports Management & Participation Platform

## Tech Stack
- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python Flask
- **Database:** SQLite
- **Auth:** Werkzeug password hashing + Flask sessions

## Project Structure
```
smart_campus_sports/
├── app.py               # Main Flask app
├── config.py            # App configuration
├── database.db          # SQLite database
├── schema.sql           # DB schema
├── requirements.txt     # Python dependencies
├── routes/              # Route handlers per role
│   ├── auth.py          # Login / Register
│   ├── admin.py         # Admin routes
│   ├── coach.py         # Coach routes
│   └── student.py       # Student routes
├── models/              # DB query helpers
│   ├── users.py
│   ├── college.py
│   ├── sports.py
│   ├── facilities.py
│   ├── trials.py
│   ├── attendance.py
│   └── performance.py
├── static/
│   ├── css/             # Stylesheets
│   ├── js/              # JavaScript files
│   └── images/          # Assets
└── templates/
    ├── base.html        # Base layout
    ├── index.html       # Landing page
    ├── login.html
    ├── register.html
    ├── admin/           # Admin templates
    ├── coach/           # Coach templates
    └── student/         # Student templates
```

## Setup Instructions
```bash
pip install -r requirements.txt
python app.py
```

## User Roles
- **Admin** — Manages college, sports, coaches, facilities, scheduling
- **Coach** — Creates trials, marks attendance, updates performance
- **Student** — Registers for trials, views timetable, tracks profile


# 📸 Project Screenshots

## 🏠 Landing Page

The landing page serves as the entry point to the Smart Campus Sports Management & Participation Platform. It provides an overview of the system, highlights key features, and allows users to navigate to the login and registration pages.

**Screenshot:** 
<img width="1918" height="915" alt="image" src="https://github.com/user-attachments/assets/e4809798-abb9-4871-8eac-9e3d561c8585" />

<img width="1912" height="918" alt="image" src="https://github.com/user-attachments/assets/103564b6-7cc3-4448-9542-3258753a8c94" />

<img width="1918" height="911" alt="image" src="https://github.com/user-attachments/assets/56a3542b-1743-4931-9aa9-60567f8fa861" />

<img width="1918" height="792" alt="image" src="https://github.com/user-attachments/assets/940bd3a6-3a10-49a6-ba76-f9b92e8d3b52" />




---

## 🔐 User Authentication

The platform provides secure user authentication using Flask sessions and Werkzeug password hashing. Users can register and log in according to their assigned roles.

### Login Page

Allows existing users to securely access their accounts.

**Screenshot:** 
<img width="1912" height="908" alt="image" src="https://github.com/user-attachments/assets/ec1e85f8-6bcd-4c4e-a92a-103d9cd94481" />



### Registration Page

New students, coaches, or administrators can create an account and join the platform.

**Screenshot:** 
<img width="1918" height="906" alt="image" src="https://github.com/user-attachments/assets/996b3a1a-093b-47b4-97d4-5c44e9c0700f" />


---

## 💾 Database Schema

The SQLite database stores user information, sports data, attendance records, trial registrations, and performance metrics.

**Screenshot:** 
<img width="1918" height="752" alt="image" src="https://github.com/user-attachments/assets/841bbcdc-c2b9-4750-872c-61934d1d9dac" />

---


