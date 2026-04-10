CREATE TABLE IF NOT EXISTS colleges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    address TEXT,
    logo TEXT,
    coordinator_name TEXT,
    coordinator_email TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    college_id INTEGER REFERENCES colleges(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    college_id INTEGER REFERENCES colleges(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    rules TEXT,
    location TEXT,
    college_id INTEGER REFERENCES colleges(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS coaches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    sport_id INTEGER REFERENCES sports(id),
    specialization TEXT,
    college_id INTEGER REFERENCES colleges(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS facilities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT,
    capacity INTEGER DEFAULT 0,
    location TEXT,
    college_id INTEGER REFERENCES colleges(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS schedules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sport_id INTEGER REFERENCES sports(id),
    facility_id INTEGER REFERENCES facilities(id),
    coach_id INTEGER REFERENCES coaches(id),
    college_id INTEGER REFERENCES colleges(id),
    date TEXT NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    session_type TEXT DEFAULT 'practice',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS trials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sport_id INTEGER REFERENCES sports(id),
    facility_id INTEGER REFERENCES facilities(id),
    coach_id INTEGER REFERENCES coaches(id),
    college_id INTEGER REFERENCES colleges(id),
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    max_participants INTEGER DEFAULT 20,
    requirements TEXT,
    status TEXT DEFAULT 'upcoming',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS trial_registrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trial_id INTEGER REFERENCES trials(id),
    student_id INTEGER REFERENCES students(id),
    status TEXT DEFAULT 'pending',
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER REFERENCES students(id),
    schedule_id INTEGER REFERENCES schedules(id),
    coach_id INTEGER REFERENCES coaches(id),
    status TEXT DEFAULT 'present',
    date TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS performance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER REFERENCES students(id),
    coach_id INTEGER REFERENCES coaches(id),
    trial_id INTEGER REFERENCES trials(id),
    speed REAL DEFAULT 0,
    agility REAL DEFAULT 0,
    skill REAL DEFAULT 0,
    teamwork REAL DEFAULT 0,
    total_score REAL DEFAULT 0,
    remarks TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(student_id, trial_id)
);

CREATE TABLE IF NOT EXISTS announcements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    college_id INTEGER REFERENCES colleges(id),
    author_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Seed data
INSERT OR IGNORE INTO colleges (id, name, address, coordinator_name, coordinator_email)
VALUES
(1, 'Hyderabad Institute of Technology', 'Hyderabad, Telangana', 'Dr. Ramesh Kumar', 'sports@hit.edu'),
(2, 'JNTU College of Engineering', 'Kukatpally, Hyderabad', 'Prof. Sita Devi', 'sports@jntu.edu'),
(3, 'Osmania University', 'Amberpet, Hyderabad', 'Dr. Venkat Rao', 'sports@ou.edu');

INSERT OR IGNORE INTO admins (id, name, email, password, college_id)
VALUES (1, 'Admin HIT', 'admin@hit.edu', 'pbkdf2:sha256:260000$rJ8sHQQ9$d9c9e0e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7e7', 1);
