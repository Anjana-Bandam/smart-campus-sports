# import os
# import sqlite3
# from flask import Flask, render_template, g
# from config import Config

# app = Flask(__name__)
# app.config.from_object(Config)

# # ---------- Database ----------
# def get_db():
#     if 'db' not in g:
#         g.db = sqlite3.connect(
#             app.config['DATABASE'],
#             detect_types=sqlite3.PARSE_DECLTYPES
#         )
#         g.db.row_factory = sqlite3.Row
#     return g.db

# def close_db(e=None):
#     db = g.pop('db', None)
#     if db is not None:
#         db.close()

# def init_db():
#     db = sqlite3.connect(app.config['DATABASE'])
#     db.row_factory = sqlite3.Row
#     with app.open_resource('schema.sql') as f:
#         db.executescript(f.read().decode('utf8'))
#     db.commit()
#     db.close()
#     print("✅ Database initialised!")

# app.teardown_appcontext(close_db)

# # ---------- Blueprints ----------
# from routes.auth import auth_bp
# from routes.student import student_bp
# from routes.coach import coach_bp
# from routes.admin import admin_bp

# app.register_blueprint(auth_bp)
# app.register_blueprint(student_bp, url_prefix='/student')
# app.register_blueprint(coach_bp,   url_prefix='/coach')
# app.register_blueprint(admin_bp,   url_prefix='/admin')

# # ---------- Landing page ----------
# @app.route('/')
# def index():
#     return render_template('index.html')

# # ---------- Run ----------
# if __name__ == '__main__':
#     if not os.path.exists(app.config['DATABASE']):
#         print("📦 No database found — creating one...")
#         init_db()
#     app.run(debug=True)
import os
import sqlite3
from flask import Flask, render_template, g
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = sqlite3.connect(app.config['DATABASE'])
    db.row_factory = sqlite3.Row
    with app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
    db.commit()
    db.close()
    print("✅ Database initialised!")

app.teardown_appcontext(close_db)

from routes.auth import auth_bp
from routes.student import student_bp
from routes.coach import coach_bp
from routes.admin import admin_bp

app.register_blueprint(auth_bp)
app.register_blueprint(student_bp, url_prefix='/student')
app.register_blueprint(coach_bp,   url_prefix='/coach')
app.register_blueprint(admin_bp,   url_prefix='/admin')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    if not os.path.exists(app.config['DATABASE']):
        print("📦 No database found — creating one...")
        init_db()
    app.run(debug=True)