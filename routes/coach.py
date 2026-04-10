from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from db import get_db
coach_bp = Blueprint('coach', __name__)

@coach_bp.route('/dashboard')
def dashboard():
    if session.get('role') != 'coach':
        return redirect(url_for('auth.login'))
    db = get_db()
    coach_id   = session['user_id']
    college_id = session['college_id']
    coach      = db.execute('SELECT * FROM coaches WHERE id=?', (coach_id,)).fetchone()
    sports     = db.execute('SELECT * FROM sports WHERE college_id=?', (college_id,)).fetchall()
    facilities = db.execute('SELECT * FROM facilities WHERE college_id=?', (college_id,)).fetchall()
    trials = db.execute('''
        SELECT t.*, s.name as sport_name, f.name as facility_name,
               (SELECT COUNT(*) FROM trial_registrations WHERE trial_id=t.id) as reg_count
        FROM trials t
        JOIN sports s ON t.sport_id=s.id
        LEFT JOIN facilities f ON t.facility_id=f.id
        WHERE t.coach_id=?
        ORDER BY t.date DESC
    ''', (coach_id,)).fetchall()
    schedules = db.execute('''
        SELECT sc.*, s.name as sport_name, f.name as facility_name
        FROM schedules sc
        JOIN sports s ON sc.sport_id=s.id
        LEFT JOIN facilities f ON sc.facility_id=f.id
        WHERE sc.coach_id=?
        ORDER BY sc.date ASC, sc.start_time ASC
    ''', (coach_id,)).fetchall()
    students = db.execute(
        'SELECT * FROM students WHERE college_id=? ORDER BY name', (college_id,)
    ).fetchall()
    # Build attendance map: {schedule_id: {student_id: status}}
    attendance_records = db.execute('''
        SELECT student_id, schedule_id, status FROM attendance
        WHERE schedule_id IN (SELECT id FROM schedules WHERE coach_id=?)
    ''', (coach_id,)).fetchall()
    attendance_map = {}
    for a in attendance_records:
        sid = a['schedule_id']
        if sid not in attendance_map:
            attendance_map[sid] = {}
        attendance_map[sid][a['student_id']] = a['status']
    return render_template('coach/dashboard.html',
        coach=coach, sports=sports, facilities=facilities,
        trials=trials, schedules=schedules, students=students,
        attendance_map=attendance_map
    )

@coach_bp.route('/trials/create', methods=['POST'])
def create_trial():
    if session.get('role') != 'coach':
        return redirect(url_for('auth.login'))
    db = get_db()
    sport_id     = request.form.get('sport_id')
    facility_id  = request.form.get('facility_id')
    date         = request.form.get('date')
    time         = request.form.get('time')
    max_p        = request.form.get('max_participants', 20)
    requirements = request.form.get('requirements', '')
    if not all([sport_id, date, time]):
        flash('Sport, date and time are required.', 'error')
        return redirect(url_for('coach.dashboard') + '?tab=trials')
    db.execute('''
        INSERT INTO trials (sport_id, facility_id, coach_id, college_id, date, time, max_participants, requirements, status)
        VALUES (?,?,?,?,?,?,?,?,'upcoming')
    ''', (sport_id, facility_id or None, session['user_id'], session['college_id'],
          date, time, max_p, requirements))
    db.commit()
    flash('Trial created successfully!', 'success')
    return redirect(url_for('coach.dashboard') + '?tab=trials')

@coach_bp.route('/trials/<int:trial_id>/registrations')
def trial_registrations(trial_id):
    if session.get('role') != 'coach':
        return redirect(url_for('auth.login'))
    db = get_db()
    trial = db.execute('''
        SELECT t.*, s.name as sport_name FROM trials t
        JOIN sports s ON t.sport_id=s.id WHERE t.id=?
    ''', (trial_id,)).fetchone()
    registrations = db.execute('''
        SELECT tr.*, st.name as student_name, st.email,
               p.speed, p.agility, p.skill, p.teamwork, p.total_score, p.remarks
        FROM trial_registrations tr
        JOIN students st ON tr.student_id=st.id
        LEFT JOIN performance p ON p.student_id=tr.student_id AND p.trial_id=tr.id
        WHERE tr.trial_id=?
        ORDER BY p.total_score DESC
    ''', (trial_id,)).fetchall()
    return render_template('coach/registrations.html', trial=trial, registrations=registrations)

@coach_bp.route('/trials/<int:trial_id>/approve/<int:student_id>', methods=['POST'])
def approve_registration(trial_id, student_id):
    if session.get('role') != 'coach':
        return redirect(url_for('auth.login'))
    db = get_db()
    db.execute('''
        UPDATE trial_registrations SET status='approved'
        WHERE trial_id=? AND student_id=?
    ''', (trial_id, student_id))
    db.commit()
    flash('Student approved!', 'success')
    return redirect(url_for('coach.trial_registrations', trial_id=trial_id))

@coach_bp.route('/performance/update', methods=['POST'])
def update_performance():
    if session.get('role') != 'coach':
        return redirect(url_for('auth.login'))
    db = get_db()
    student_id = request.form.get('student_id')
    trial_id   = request.form.get('trial_id')
    speed      = float(request.form.get('speed', 0))
    agility    = float(request.form.get('agility', 0))
    skill      = float(request.form.get('skill', 0))
    teamwork   = float(request.form.get('teamwork', 0))
    remarks    = request.form.get('remarks', '')
    total      = round((speed + agility + skill + teamwork) / 4, 2)
    existing = db.execute(
        'SELECT id FROM performance WHERE student_id=? AND trial_id=?',
        (student_id, trial_id)
    ).fetchone()
    if existing:
        db.execute('''
            UPDATE performance SET speed=?, agility=?, skill=?, teamwork=?,
            total_score=?, remarks=? WHERE student_id=? AND trial_id=?
        ''', (speed, agility, skill, teamwork, total, remarks, student_id, trial_id))
    else:
        db.execute('''
            INSERT INTO performance (student_id, coach_id, trial_id, speed, agility, skill, teamwork, total_score, remarks)
            VALUES (?,?,?,?,?,?,?,?,?)
        ''', (student_id, session['user_id'], trial_id, speed, agility, skill, teamwork, total, remarks))
    db.commit()
    flash('Performance updated!', 'success')
    return redirect(url_for('coach.trial_registrations', trial_id=trial_id))

@coach_bp.route('/schedule/create', methods=['POST'])
def create_schedule():
    if session.get('role') != 'coach':
        return redirect(url_for('auth.login'))
    db = get_db()
    sport_id     = request.form.get('sport_id')
    facility_id  = request.form.get('facility_id')
    date         = request.form.get('date')
    start_time   = request.form.get('start_time')
    end_time     = request.form.get('end_time')
    session_type = request.form.get('session_type', 'practice')
    if not all([sport_id, date, start_time, end_time]):
        flash('Sport, date and times are required.', 'error')
        return redirect(url_for('coach.dashboard') + '?tab=schedule')
    if facility_id:
        conflict = db.execute('''
            SELECT id FROM schedules
            WHERE facility_id=? AND date=?
            AND NOT (end_time <= ? OR start_time >= ?)
        ''', (facility_id, date, start_time, end_time)).fetchone()
        if conflict:
            flash('⚠️ Conflict! That venue is already booked at this time.', 'error')
            return redirect(url_for('coach.dashboard') + '?tab=schedule')
    db.execute('''
        INSERT INTO schedules (sport_id, facility_id, coach_id, college_id, date, start_time, end_time, session_type)
        VALUES (?,?,?,?,?,?,?,?)
    ''', (sport_id, facility_id or None, session['user_id'], session['college_id'],
          date, start_time, end_time, session_type))
    db.commit()
    flash('Schedule created!', 'success')
    return redirect(url_for('coach.dashboard') + '?tab=schedule')

@coach_bp.route('/attendance/mark', methods=['POST'])
def mark_attendance():
    if session.get('role') != 'coach':
        return redirect(url_for('auth.login'))
    db = get_db()
    schedule_id = request.form.get('schedule_id')
    present_ids = request.form.getlist('present')
    students = db.execute(
        'SELECT id FROM students WHERE college_id=?', (session['college_id'],)
    ).fetchall()
    for s in students:
        sid    = str(s['id'])
        status = 'present' if sid in present_ids else 'absent'
        existing = db.execute(
            'SELECT id FROM attendance WHERE student_id=? AND schedule_id=?',
            (sid, schedule_id)
        ).fetchone()
        if existing:
            db.execute('UPDATE attendance SET status=? WHERE student_id=? AND schedule_id=?',
                       (status, sid, schedule_id))
        else:
            db.execute('''
                INSERT INTO attendance (student_id, schedule_id, coach_id, status, date)
                VALUES (?,?,?,?,DATE("now"))
            ''', (sid, schedule_id, session['user_id'], status))
    db.commit()
    flash('Attendance marked!', 'success')
    return redirect(url_for('coach.dashboard') + '?tab=attendance')