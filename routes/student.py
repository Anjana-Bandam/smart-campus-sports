# # from flask import Blueprint
# # student_bp = Blueprint('student', __name__)


# from flask import Blueprint, render_template, session, redirect, url_for
# from db import get_db

# student_bp = Blueprint('student', __name__)

# @student_bp.route('/dashboard')
# def dashboard():
#     if session.get('role') != 'student':
#         return redirect(url_for('auth.login'))
#     return render_template('student/dashboard.html')
from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from db import get_db

student_bp = Blueprint('student', __name__)

@student_bp.route('/dashboard')
def dashboard():
    if session.get('role') != 'student':
        return redirect(url_for('auth.login'))
    
    db = get_db()
    student_id = session['user_id']
    college_id = session['college_id']

    # Sports in their college
    sports = db.execute(
        'SELECT * FROM sports WHERE college_id = ?', (college_id,)
    ).fetchall()

    # Upcoming trials
    trials = db.execute('''
        SELECT t.*, s.name as sport_name, c.name as coach_name
        FROM trials t
        JOIN sports s ON t.sport_id = s.id
        LEFT JOIN coaches c ON t.coach_id = c.id
        WHERE t.college_id = ? AND t.status = "upcoming"
        ORDER BY t.date ASC LIMIT 5
    ''', (college_id,)).fetchall()

    # Their trial registrations
    my_registrations = db.execute('''
        SELECT tr.*, t.date, t.time, s.name as sport_name, tr.status
        FROM trial_registrations tr
        JOIN trials t ON tr.trial_id = t.id
        JOIN sports s ON t.sport_id = s.id
        WHERE tr.student_id = ?
        ORDER BY t.date DESC LIMIT 5
    ''', (student_id,)).fetchall()

    # Upcoming schedules
    schedules = db.execute('''
        SELECT sc.*, s.name as sport_name, f.name as facility_name
        FROM schedules sc
        JOIN sports s ON sc.sport_id = s.id
        LEFT JOIN facilities f ON sc.facility_id = f.id
        WHERE sc.college_id = ?
        ORDER BY sc.date ASC, sc.start_time ASC LIMIT 6
    ''', (college_id,)).fetchall()

    # Announcements
    announcements = db.execute('''
        SELECT * FROM announcements
        WHERE college_id = ?
        ORDER BY created_at DESC LIMIT 4
    ''', (college_id,)).fetchall()

    # Attendance stats
    total_sessions = db.execute(
        'SELECT COUNT(*) as cnt FROM attendance WHERE student_id = ?', (student_id,)
    ).fetchone()['cnt']
    present_sessions = db.execute(
        'SELECT COUNT(*) as cnt FROM attendance WHERE student_id = ? AND status = "present"', (student_id,)
    ).fetchone()['cnt']
    attendance_pct = round((present_sessions / total_sessions * 100) if total_sessions > 0 else 0)

    # Performance
    performance = db.execute('''
        SELECT p.*, sp.name as sport_name
        FROM performance p
        LEFT JOIN trials t ON p.trial_id = t.id
        LEFT JOIN sports sp ON t.sport_id = sp.id
        WHERE p.student_id = ?
        ORDER BY p.created_at DESC LIMIT 1
    ''', (student_id,)).fetchone()

    return render_template('student/dashboard.html',
        sports=sports,
        trials=trials,
        my_registrations=my_registrations,
        schedules=schedules,
        announcements=announcements,
        attendance_pct=attendance_pct,
        total_sessions=total_sessions,
        performance=performance
    )


@student_bp.route('/trials')
def trials():
    if session.get('role') != 'student':
        return redirect(url_for('auth.login'))
    db = get_db()
    college_id = session['college_id']
    student_id = session['user_id']

    all_trials = db.execute('''
        SELECT t.*, s.name as sport_name, c.name as coach_name,
               (SELECT COUNT(*) FROM trial_registrations WHERE trial_id = t.id) as registered_count,
               (SELECT status FROM trial_registrations WHERE trial_id = t.id AND student_id = ?) as my_status
        FROM trials t
        JOIN sports s ON t.sport_id = s.id
        LEFT JOIN coaches c ON t.coach_id = c.id
        WHERE t.college_id = ?
        ORDER BY t.date ASC
    ''', (student_id, college_id)).fetchall()

    return render_template('student/trials.html', trials=all_trials)


@student_bp.route('/trials/register/<int:trial_id>', methods=['POST'])
def register_trial(trial_id):
    if session.get('role') != 'student':
        return redirect(url_for('auth.login'))
    db = get_db()
    student_id = session['user_id']

    # Check already registered
    existing = db.execute(
        'SELECT id FROM trial_registrations WHERE trial_id=? AND student_id=?',
        (trial_id, student_id)
    ).fetchone()
    if existing:
        flash('You are already registered for this trial.', 'error')
        return redirect(url_for('student.trials'))

    # Check capacity
    trial = db.execute('SELECT * FROM trials WHERE id=?', (trial_id,)).fetchone()
    count = db.execute(
        'SELECT COUNT(*) as cnt FROM trial_registrations WHERE trial_id=?', (trial_id,)
    ).fetchone()['cnt']

    status = 'waitlisted' if count >= trial['max_participants'] else 'pending'

    db.execute(
        'INSERT INTO trial_registrations (trial_id, student_id, status) VALUES (?,?,?)',
        (trial_id, student_id, status)
    )
    db.commit()
    flash(f'Registered! Status: {status.capitalize()}.', 'success')
    return redirect(url_for('student.trials'))


@student_bp.route('/profile')
def profile():
    if session.get('role') != 'student':
        return redirect(url_for('auth.login'))
    db = get_db()
    student_id = session['user_id']

    student = db.execute(
        'SELECT s.*, c.name as college_name FROM students s JOIN colleges c ON s.college_id = c.id WHERE s.id=?',
        (student_id,)
    ).fetchone()

    performances = db.execute('''
        SELECT p.*, sp.name as sport_name
        FROM performance p
        LEFT JOIN trials t ON p.trial_id = t.id
        LEFT JOIN sports sp ON t.sport_id = sp.id
        WHERE p.student_id = ? ORDER BY p.created_at DESC
    ''', (student_id,)).fetchall()

    registrations = db.execute('''
        SELECT tr.*, t.date, t.time, s.name as sport_name
        FROM trial_registrations tr
        JOIN trials t ON tr.trial_id = t.id
        JOIN sports s ON t.sport_id = s.id
        WHERE tr.student_id = ? ORDER BY t.date DESC
    ''', (student_id,)).fetchall()

    return render_template('student/profile.html',
        student=student,
        performances=performances,
        registrations=registrations
    )