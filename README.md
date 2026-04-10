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
