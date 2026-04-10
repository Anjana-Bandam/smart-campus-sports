from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from db import get_db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
def dashboard():
    if session.get('role') != 'admin':
        return redirect(url_for('auth.login'))
    db = get_db()
    college_id = session['college_id']

    college = db.execute('SELECT * FROM colleges WHERE id=?', (college_id,)).fetchone()
    sports_count = db.execute('SELECT COUNT(*) as cnt FROM sports WHERE college_id=?', (college_id,)).fetchone()['cnt']
    coaches_count = db.execute('SELECT COUNT(*) as cnt FROM coaches WHERE college_id=?', (college_id,)).fetchone()['cnt']
    students_count = db.execute('SELECT COUNT(*) as cnt FROM students WHERE college_id=?', (college_id,)).fetchone()['cnt']
    facilities_count = db.execute('SELECT COUNT(*) as cnt FROM facilities WHERE college_id=?', (college_id,)).fetchone()['cnt']

    sports = db.execute('SELECT * FROM sports WHERE college_id=? ORDER BY created_at DESC', (college_id,)).fetchall()
    coaches = db.execute('''
        SELECT c.*, s.name as sport_name
        FROM coaches c
        LEFT JOIN sports s ON c.sport_id = s.id
        WHERE c.college_id=?
        ORDER BY c.created_at DESC
    ''', (college_id,)).fetchall()
    facilities = db.execute('SELECT * FROM facilities WHERE college_id=? ORDER BY created_at DESC', (college_id,)).fetchall()
    announcements = db.execute('SELECT * FROM announcements WHERE college_id=? ORDER BY created_at DESC LIMIT 10', (college_id,)).fetchall()
    recent_students = db.execute('SELECT * FROM students WHERE college_id=? ORDER BY created_at DESC LIMIT 10', (college_id,)).fetchall()
    recent_registrations = db.execute('''
        SELECT tr.*, s.name as student_name, sp.name as sport_name, t.date
        FROM trial_registrations tr
        JOIN students s ON tr.student_id = s.id
        JOIN trials t ON tr.trial_id = t.id
        JOIN sports sp ON t.sport_id = sp.id
        WHERE t.college_id=?
        ORDER BY tr.registered_at DESC LIMIT 10
    ''', (college_id,)).fetchall()

    return render_template('admin/dashboard.html',
        college=college,
        sports=sports, coaches=coaches,
        facilities=facilities, announcements=announcements,
        recent_students=recent_students,
        recent_registrations=recent_registrations,
        sports_count=sports_count, coaches_count=coaches_count,
        students_count=students_count, facilities_count=facilities_count
    )

# ── SPORTS ──────────────────────────────────────────
@admin_bp.route('/sports/add', methods=['POST'])
def add_sport():
    if session.get('role') != 'admin':
        return redirect(url_for('auth.login'))
    db = get_db()
    name        = request.form.get('name', '').strip()
    description = request.form.get('description', '').strip()
    location    = request.form.get('location', '').strip()
    if not name:
        flash('Sport name is required.', 'error')
        return redirect(url_for('admin.dashboard') + '?tab=sports')
    db.execute('INSERT INTO sports (name, description, location, college_id) VALUES (?,?,?,?)',
               (name, description, location, session['college_id']))
    db.commit()
    flash(f'Sport "{name}" added successfully!', 'success')
    return redirect(url_for('admin.dashboard') + '?tab=sports')

@admin_bp.route('/sports/delete/<int:sport_id>', methods=['POST'])
def delete_sport(sport_id):
    if session.get('role') != 'admin':
        return redirect(url_for('auth.login'))
    db = get_db()
    db.execute('DELETE FROM sports WHERE id=? AND college_id=?', (sport_id, session['college_id']))
    db.commit()
    flash('Sport deleted.', 'success')
    return redirect(url_for('admin.dashboard') + '?tab=sports')

# ── COACHES ─────────────────────────────────────────
@admin_bp.route('/coaches/add', methods=['POST'])
def add_coach():
    if session.get('role') != 'admin':
        return redirect(url_for('auth.login'))
    from werkzeug.security import generate_password_hash
    db = get_db()
    name     = request.form.get('name', '').strip()
    email    = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '').strip()
    sport_id = request.form.get('sport_id')
    if not all([name, email, password]):
        flash('Name, email and password are required.', 'error')
        return redirect(url_for('admin.dashboard') + '?tab=coaches')
    existing = db.execute('SELECT id FROM coaches WHERE email=?', (email,)).fetchone()
    if existing:
        flash('A coach with this email already exists.', 'error')
        return redirect(url_for('admin.dashboard') + '?tab=coaches')
    db.execute('INSERT INTO coaches (name, email, password, sport_id, college_id) VALUES (?,?,?,?,?)',
               (name, email, generate_password_hash(password), sport_id or None, session['college_id']))
    db.commit()
    flash(f'Coach "{name}" added! They can login with {email}.', 'success')
    return redirect(url_for('admin.dashboard') + '?tab=coaches')

@admin_bp.route('/coaches/delete/<int:coach_id>', methods=['POST'])
def delete_coach(coach_id):
    if session.get('role') != 'admin':
        return redirect(url_for('auth.login'))
    db = get_db()
    db.execute('DELETE FROM coaches WHERE id=? AND college_id=?', (coach_id, session['college_id']))
    db.commit()
    flash('Coach removed.', 'success')
    return redirect(url_for('admin.dashboard') + '?tab=coaches')

# ── FACILITIES ───────────────────────────────────────
@admin_bp.route('/facilities/add', methods=['POST'])
def add_facility():
    if session.get('role') != 'admin':
        return redirect(url_for('auth.login'))
    db = get_db()
    name     = request.form.get('name', '').strip()
    type_    = request.form.get('type', '').strip()
    capacity = request.form.get('capacity', 0)
    location = request.form.get('location', '').strip()
    if not name:
        flash('Facility name is required.', 'error')
        return redirect(url_for('admin.dashboard') + '?tab=facilities')
    db.execute('INSERT INTO facilities (name, type, capacity, location, college_id) VALUES (?,?,?,?,?)',
               (name, type_, capacity, location, session['college_id']))
    db.commit()
    flash(f'Facility "{name}" added!', 'success')
    return redirect(url_for('admin.dashboard') + '?tab=facilities')

@admin_bp.route('/facilities/delete/<int:fid>', methods=['POST'])
def delete_facility(fid):
    if session.get('role') != 'admin':
        return redirect(url_for('auth.login'))
    db = get_db()
    db.execute('DELETE FROM facilities WHERE id=? AND college_id=?', (fid, session['college_id']))
    db.commit()
    flash('Facility deleted.', 'success')
    return redirect(url_for('admin.dashboard') + '?tab=facilities')

# ── ANNOUNCEMENTS ────────────────────────────────────
@admin_bp.route('/announcements/add', methods=['POST'])
def add_announcement():
    if session.get('role') != 'admin':
        return redirect(url_for('auth.login'))
    db = get_db()
    title   = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()
    if not all([title, content]):
        flash('Title and content are required.', 'error')
        return redirect(url_for('admin.dashboard') + '?tab=announce')
    db.execute('INSERT INTO announcements (title, content, college_id, author_id) VALUES (?,?,?,?)',
               (title, content, session['college_id'], session['user_id']))
    db.commit()
    flash('Announcement posted!', 'success')
    return redirect(url_for('admin.dashboard') + '?tab=announce')

@admin_bp.route('/announcements/delete/<int:aid>', methods=['POST'])
def delete_announcement(aid):
    if session.get('role') != 'admin':
        return redirect(url_for('auth.login'))
    db = get_db()
    db.execute('DELETE FROM announcements WHERE id=? AND college_id=?', (aid, session['college_id']))
    db.commit()
    flash('Announcement deleted.', 'success')
    return redirect(url_for('admin.dashboard') + '?tab=announce')