# from flask import Blueprint, render_template, request, redirect, url_for, session, flash
# import sqlite3
# from werkzeug.security import generate_password_hash, check_password_hash
# from db import get_db

# auth_bp = Blueprint('auth', __name__)

# # ── helpers ──────────────────────────────────────────
# def login_required(f):
#     from functools import wraps
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         if 'user_id' not in session:
#             return redirect(url_for('auth.login'))
#         return f(*args, **kwargs)
#     return decorated

# # ── LOGIN ─────────────────────────────────────────────
# @auth_bp.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email    = request.form.get('email', '').strip().lower()
#         password = request.form.get('password', '')
#         role     = request.form.get('role', '')

#         db = get_db()
#         user = None

#         if role == 'admin':
#             user = db.execute('SELECT * FROM admins WHERE email = ?', (email,)).fetchone()
#         elif role == 'coach':
#             user = db.execute('SELECT * FROM coaches WHERE email = ?', (email,)).fetchone()
#         elif role == 'student':
#             user = db.execute('SELECT * FROM students WHERE email = ?', (email,)).fetchone()

#         if user and check_password_hash(user['password'], password):
#             session.clear()
#             session['user_id']   = user['id']
#             session['user_name'] = user['name']
#             session['role']      = role
#             session['college_id'] = user['college_id']

#             if role == 'admin':
#                 return redirect(url_for('admin.dashboard'))
#             elif role == 'coach':
#                 return redirect(url_for('coach.dashboard'))
#             else:
#                 return redirect(url_for('student.dashboard'))
#         else:
#             flash('Invalid email, password or role.', 'error')

#     return render_template('login.html')


# # ── REGISTER (students only) ──────────────────────────
# @auth_bp.route('/register', methods=['GET', 'POST'])
# def register():
#     db = get_db()
#     colleges = db.execute('SELECT id, name FROM colleges ORDER BY name').fetchall()

#     if request.method == 'POST':
#         name       = request.form.get('name', '').strip()
#         email      = request.form.get('email', '').strip().lower()
#         password   = request.form.get('password', '')
#         college_id = request.form.get('college_id')

#         if not all([name, email, password, college_id]):
#             flash('Please fill in all fields.', 'error')
#             return render_template('register.html', colleges=colleges)

#         existing = db.execute('SELECT id FROM students WHERE email = ?', (email,)).fetchone()
#         if existing:
#             flash('An account with this email already exists.', 'error')
#             return render_template('register.html', colleges=colleges)

#         hashed = generate_password_hash(password)
#         db.execute(
#             'INSERT INTO students (name, email, password, college_id) VALUES (?, ?, ?, ?)',
#             (name, email, hashed, college_id)
#         )
#         db.commit()
#         flash('Account created! Please log in.', 'success')
#         return redirect(url_for('auth.login'))

#     return render_template('register.html', colleges=colleges)


# # ── LOGOUT ────────────────────────────────────────────
# @auth_bp.route('/logout')
# def logout():
#     session.clear()
#     return redirect(url_for('index'))
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db

auth_bp = Blueprint('auth', __name__)

# ── LOGIN ─────────────────────────────────────────────
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        role     = request.form.get('role', '')

        db   = get_db()
        user = None

        if role == 'admin':
            user = db.execute('SELECT * FROM admins WHERE email=?', (email,)).fetchone()
        elif role == 'coach':
            user = db.execute('SELECT * FROM coaches WHERE email=?', (email,)).fetchone()
        elif role == 'student':
            user = db.execute('SELECT * FROM students WHERE email=?', (email,)).fetchone()

        if user and check_password_hash(user['password'], password):
            session.clear()
            session['user_id']    = user['id']
            session['user_name']  = user['name']
            session['role']       = role
            session['college_id'] = user['college_id']

            if role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif role == 'coach':
                return redirect(url_for('coach.dashboard'))
            else:
                return redirect(url_for('student.dashboard'))
        else:
            flash('Invalid email, password or role.', 'error')

    return render_template('login.html')


# ── STUDENT REGISTER ──────────────────────────────────
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    db       = get_db()
    colleges = db.execute('SELECT id, name FROM colleges ORDER BY name').fetchall()

    if request.method == 'POST':
        name       = request.form.get('name', '').strip()
        email      = request.form.get('email', '').strip().lower()
        password   = request.form.get('password', '')
        college_id = request.form.get('college_id')

        if not all([name, email, password, college_id]):
            flash('Please fill in all fields.', 'error')
            return render_template('register.html', colleges=colleges)

        existing = db.execute('SELECT id FROM students WHERE email=?', (email,)).fetchone()
        if existing:
            flash('An account with this email already exists.', 'error')
            return render_template('register.html', colleges=colleges)

        db.execute(
            'INSERT INTO students (name, email, password, college_id) VALUES (?,?,?,?)',
            (name, email, generate_password_hash(password), college_id)
        )
        db.commit()
        flash('Account created! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html', colleges=colleges)


# ── COLLEGE REGISTER (admin signup) ───────────────────
@auth_bp.route('/register-college', methods=['GET', 'POST'])
def register_college():
    db = get_db()
    colleges = db.execute(
        'SELECT name FROM colleges WHERE id NOT IN (SELECT college_id FROM admins WHERE college_id IS NOT NULL) ORDER BY name'
    ).fetchall()

    if request.method == 'POST':
        college_name   = request.form.get('college_name', '').strip()
        address        = request.form.get('address', '').strip()
        admin_name     = request.form.get('admin_name', '').strip()
        admin_email    = request.form.get('admin_email', '').strip().lower()
        admin_password = request.form.get('admin_password', '')

        if not all([college_name, admin_name, admin_email, admin_password]):
            flash('Please fill in all required fields.', 'error')
            return render_template('register_college.html', colleges=colleges)

        # Check if college already has an admin
        existing_college = db.execute(
            'SELECT id FROM colleges WHERE LOWER(name)=?',
            (college_name.lower(),)
        ).fetchone()

        if existing_college:
            already_has_admin = db.execute(
                'SELECT id FROM admins WHERE college_id=?',
                (existing_college['id'],)
            ).fetchone()
            if already_has_admin:
                flash('This college is already registered. Contact your existing admin.', 'error')
                return render_template('register_college.html', colleges=colleges)

        # Check if admin email already used
        existing_admin = db.execute(
            'SELECT id FROM admins WHERE email=?', (admin_email,)
        ).fetchone()
        if existing_admin:
            flash('An admin account with this email already exists.', 'error')
            return render_template('register_college.html', colleges=colleges)

        # Get college id
        college = db.execute(
            'SELECT id FROM colleges WHERE name=?', (college_name,)
        ).fetchone()

        if not college:
            flash('College not found. Please select from the list.', 'error')
            return render_template('register_college.html', colleges=colleges)

        # Create admin for that college
        db.execute(
            'INSERT INTO admins (name, email, password, college_id) VALUES (?,?,?,?)',
            (admin_name, admin_email, generate_password_hash(admin_password), college['id'])
        )
        db.commit()

        flash('College registered successfully! You can now log in as Admin.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register_college.html', colleges=colleges)


# ── LOGOUT ────────────────────────────────────────────
@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))