from app import app
from db import get_db
from werkzeug.security import generate_password_hash

with app.app_context():
    db = get_db()

    # Get college IDs
    cbit   = db.execute('SELECT id FROM colleges WHERE name LIKE "%Chaitanya Bharathi%"').fetchone()
    vasavi = db.execute('SELECT id FROM colleges WHERE name LIKE "%Vasavi%"').fetchone()
    cbit_id   = cbit['id']
    vasavi_id = vasavi['id']
    print(f'CBIT id: {cbit_id}, Vasavi id: {vasavi_id}')

    # ── ADMINS ──
    db.execute('INSERT OR IGNORE INTO admins (name, email, password, college_id) VALUES (?,?,?,?)',
        ('Ramesh Kumar', 'ramesh@gmail.com', generate_password_hash('ramesh123'), cbit_id))

    # ── SPORTS ──
    sport_names = ['Cricket', 'Football', 'Basketball', 'Badminton', 'Tennis']

    cbit_sport_ids = []
    for s in sport_names:
        db.execute('INSERT INTO sports (name, college_id, location) VALUES (?,?,?)',
            (s, cbit_id, f'{s} Ground - CBIT'))
        sid = db.execute('SELECT id FROM sports WHERE name=? AND college_id=? ORDER BY id DESC LIMIT 1',
            (s, cbit_id)).fetchone()['id']
        cbit_sport_ids.append(sid)

    vasavi_sport_ids = []
    for s in sport_names:
        db.execute('INSERT INTO sports (name, college_id, location) VALUES (?,?,?)',
            (s, vasavi_id, f'{s} Ground - Vasavi'))
        sid = db.execute('SELECT id FROM sports WHERE name=? AND college_id=? ORDER BY id DESC LIMIT 1',
            (s, vasavi_id)).fetchone()['id']
        vasavi_sport_ids.append(sid)

    db.commit()

    # ── FACILITIES ──
    cbit_facilities = [
        ('Main Cricket Ground', 'Ground', 100, 'Block A - CBIT'),
        ('Football Field',      'Ground', 80,  'Block B - CBIT'),
        ('Basketball Court',    'Court',  30,  'Block C - CBIT'),
        ('Badminton Hall',      'Hall',   20,  'Indoor Block - CBIT'),
        ('Tennis Court',        'Court',  20,  'Block D - CBIT'),
    ]
    vasavi_facilities = [
        ('Main Cricket Ground', 'Ground', 100, 'Block A - Vasavi'),
        ('Football Field',      'Ground', 80,  'Block B - Vasavi'),
        ('Basketball Court',    'Court',  30,  'Block C - Vasavi'),
        ('Badminton Hall',      'Hall',   20,  'Indoor Block - Vasavi'),
        ('Tennis Court',        'Court',  20,  'Block D - Vasavi'),
    ]

    cbit_fac_ids = []
    for name, type_, cap, loc in cbit_facilities:
        db.execute('INSERT INTO facilities (name, type, capacity, location, college_id) VALUES (?,?,?,?,?)',
            (name, type_, cap, loc, cbit_id))
        fid = db.execute('SELECT id FROM facilities WHERE name=? AND college_id=? ORDER BY id DESC LIMIT 1',
            (name, cbit_id)).fetchone()['id']
        cbit_fac_ids.append(fid)

    vasavi_fac_ids = []
    for name, type_, cap, loc in vasavi_facilities:
        db.execute('INSERT INTO facilities (name, type, capacity, location, college_id) VALUES (?,?,?,?,?)',
            (name, type_, cap, loc, vasavi_id))
        fid = db.execute('SELECT id FROM facilities WHERE name=? AND college_id=? ORDER BY id DESC LIMIT 1',
            (name, vasavi_id)).fetchone()['id']
        vasavi_fac_ids.append(fid)

    db.commit()

    # ── COACHES ──
    cbit_coaches = [
        ('Arjun Reddy',   'arjun@gmail.com',   'arjun123',   0),
        ('Priya Sharma',  'priya@gmail.com',    'priya123',   0),
        ('Karan Mehta',   'karan@gmail.com',    'karan123',   1),
        ('Sneha Rao',     'sneha@gmail.com',    'sneha123',   1),
        ('Vikram Singh',  'vikram@gmail.com',   'vikram123',  2),
        ('Divya Nair',    'divya@gmail.com',    'divya123',   2),
        ('Rohit Verma',   'rohit@gmail.com',    'rohit123',   3),
        ('Anjali Gupta',  'anjali@gmail.com',   'anjali123',  3),
        ('Suresh Patil',  'suresh@gmail.com',   'suresh123',  4),
        ('Meena Iyer',    'meena@gmail.com',    'meena123',   4),
    ]
    vasavi_coaches = [
        ('Rahul Kumar',   'rahul@gmail.com',    'rahul123',   0),
        ('Lakshmi Devi',  'lakshmi@gmail.com',  'lakshmi123', 0),
        ('Aditya Nair',   'aditya@gmail.com',   'aditya123',  1),
        ('Pooja Reddy',   'pooja@gmail.com',    'pooja123',   1),
        ('Sanjay Sharma', 'sanjay@gmail.com',   'sanjay123',  2),
        ('Kavitha Rao',   'kavitha@gmail.com',  'kavitha123', 2),
        ('Manoj Tiwari',  'manoj@gmail.com',    'manoj123',   3),
        ('Deepa Menon',   'deepa@gmail.com',    'deepa123',   3),
        ('Ravi Shankar',  'ravi@gmail.com',     'ravi123',    4),
        ('Sunita Pillai', 'sunita@gmail.com',   'sunita123',  4),
    ]

    cbit_coach_ids = []
    for name, email, pwd, sport_idx in cbit_coaches:
        db.execute('INSERT OR IGNORE INTO coaches (name, email, password, sport_id, college_id) VALUES (?,?,?,?,?)',
            (name, email, generate_password_hash(pwd), cbit_sport_ids[sport_idx], cbit_id))
        cid = db.execute('SELECT id FROM coaches WHERE email=?', (email,)).fetchone()['id']
        cbit_coach_ids.append((cid, sport_idx))

    vasavi_coach_ids = []
    for name, email, pwd, sport_idx in vasavi_coaches:
        db.execute('INSERT OR IGNORE INTO coaches (name, email, password, sport_id, college_id) VALUES (?,?,?,?,?)',
            (name, email, generate_password_hash(pwd), vasavi_sport_ids[sport_idx], vasavi_id))
        cid = db.execute('SELECT id FROM coaches WHERE email=?', (email,)).fetchone()['id']
        vasavi_coach_ids.append((cid, sport_idx))

    db.commit()

    # ── STUDENTS ──
    cbit_students = [
        ('Aarav Shah',     'aarav@gmail.com',     'aarav123'),
        ('Bhavya Reddy',   'bhavya@gmail.com',    'bhavya123'),
        ('Charan Kumar',   'charan@gmail.com',    'charan123'),
        ('Diya Sharma',    'diya@gmail.com',      'diya123'),
        ('Eshan Mehta',    'eshan@gmail.com',     'eshan123'),
        ('Fiza Khan',      'fiza@gmail.com',      'fiza123'),
        ('Ganesh Rao',     'ganesh@gmail.com',    'ganesh123'),
        ('Harini Nair',    'harini@gmail.com',    'harini123'),
        ('Ishaan Verma',   'ishaan@gmail.com',    'ishaan123'),
        ('Jhanvi Gupta',   'jhanvi@gmail.com',    'jhanvi123'),
    ]
    vasavi_students = [
        ('Kiran Patil',    'kiran@gmail.com',     'kiran123'),
        ('Lavanya Iyer',   'lavanya@gmail.com',   'lavanya123'),
        ('Manish Kumar',   'manish@gmail.com',    'manish123'),
        ('Nandini Rao',    'nandini@gmail.com',   'nandini123'),
        ('Om Sharma',      'om@gmail.com',        'om123'),
        ('Pallavi Reddy',  'pallavi@gmail.com',   'pallavi123'),
        ('Qasim Khan',     'qasim@gmail.com',     'qasim123'),
        ('Riya Mehta',     'riya@gmail.com',      'riya123'),
        ('Siddharth Nair', 'siddharth@gmail.com', 'siddharth123'),
        ('Tanvi Gupta',    'tanvi@gmail.com',     'tanvi123'),
    ]

    for name, email, pwd in cbit_students:
        db.execute('INSERT OR IGNORE INTO students (name, email, password, college_id) VALUES (?,?,?,?)',
            (name, email, generate_password_hash(pwd), cbit_id))

    for name, email, pwd in vasavi_students:
        db.execute('INSERT OR IGNORE INTO students (name, email, password, college_id) VALUES (?,?,?,?)',
            (name, email, generate_password_hash(pwd), vasavi_id))

    db.commit()

    # ── TRIALS ──
    trial_dates = ['2026-04-15', '2026-04-17', '2026-04-19', '2026-04-21', '2026-04-23']
    trial_times = ['09:00',      '10:00',      '11:00',      '09:30',      '10:30']

    for i, (coach_id, sport_idx) in enumerate(cbit_coach_ids[::2]):
        db.execute('''INSERT INTO trials
            (sport_id, facility_id, coach_id, college_id, date, time, max_participants, requirements, status)
            VALUES (?,?,?,?,?,?,?,?,?)''',
            (cbit_sport_ids[sport_idx], cbit_fac_ids[sport_idx], coach_id,
             cbit_id, trial_dates[i], trial_times[i], 20, 'Bring sports kit', 'upcoming'))

    for i, (coach_id, sport_idx) in enumerate(vasavi_coach_ids[::2]):
        db.execute('''INSERT INTO trials
            (sport_id, facility_id, coach_id, college_id, date, time, max_participants, requirements, status)
            VALUES (?,?,?,?,?,?,?,?,?)''',
            (vasavi_sport_ids[sport_idx], vasavi_fac_ids[sport_idx], coach_id,
             vasavi_id, trial_dates[i], trial_times[i], 20, 'Bring sports kit', 'upcoming'))

    db.commit()

    # ── SCHEDULES ──
    sched_dates  = ['2026-04-14', '2026-04-16', '2026-04-18', '2026-04-20', '2026-04-22']
    start_times  = ['07:00', '08:00', '07:30', '08:30', '07:00']
    end_times    = ['09:00', '10:00', '09:30', '10:30', '09:00']

    for i, (coach_id, sport_idx) in enumerate(cbit_coach_ids[1::2]):
        db.execute('''INSERT INTO schedules
            (sport_id, facility_id, coach_id, college_id, date, start_time, end_time, session_type)
            VALUES (?,?,?,?,?,?,?,?)''',
            (cbit_sport_ids[sport_idx], cbit_fac_ids[sport_idx], coach_id,
             cbit_id, sched_dates[i], start_times[i], end_times[i], 'practice'))

    for i, (coach_id, sport_idx) in enumerate(vasavi_coach_ids[1::2]):
        db.execute('''INSERT INTO schedules
            (sport_id, facility_id, coach_id, college_id, date, start_time, end_time, session_type)
            VALUES (?,?,?,?,?,?,?,?)''',
            (vasavi_sport_ids[sport_idx], vasavi_fac_ids[sport_idx], coach_id,
             vasavi_id, sched_dates[i], start_times[i], end_times[i], 'practice'))

    db.commit()

    # ── ANNOUNCEMENTS ──
    cbit_admin   = db.execute('SELECT id FROM admins WHERE college_id=?', (cbit_id,)).fetchone()
    vasavi_admin = db.execute('SELECT id FROM admins WHERE college_id=?', (vasavi_id,)).fetchone()

    for title, content in [
        ('Cricket Trials This Week',  'Cricket trials on April 15. Register before April 14.'),
        ('New Basketball Court Open', 'Renovated basketball court in Block C is now open.'),
        ('Sports Day Announced',      'Annual Sports Day on May 10. All teams must participate.'),
    ]:
        db.execute('INSERT INTO announcements (title, content, college_id, author_id) VALUES (?,?,?,?)',
            (title, content, cbit_id, cbit_admin['id']))

    for title, content in [
        ('Football Trials Announced',      'Football trials on April 15. Register on the portal.'),
        ('Badminton Practice Rescheduled', 'Badminton practice moved to 8 AM. Update your schedules.'),
        ('Welcome to SportsCampus',        'Vasavi College is now on SportsCampus! Register today.'),
    ]:
        db.execute('INSERT INTO announcements (title, content, college_id, author_id) VALUES (?,?,?,?)',
            (title, content, vasavi_id, vasavi_admin['id']))

    db.commit()

    print('✅ All done! Summary:')
    print(f'   Colleges : CBIT (id {cbit_id}), Vasavi (id {vasavi_id})')
    print(f'   Sports   : 5 per college')
    print(f'   Coaches  : 10 per college (2 per sport)')
    print(f'   Students : 10 per college')
    print(f'   Trials   : 5 per college')
    print(f'   Schedules: 5 per college')
    print(f'   Announce : 3 per college')