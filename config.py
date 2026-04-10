import os
from datetime import timedelta


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'sportscampus-dev-key-change-in-production')
    DATABASE    = os.path.join(os.path.dirname(__file__), 'database.db')

    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # File uploads (if needed)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

    # App settings
    APP_NAME    = 'SportsCampus'
    APP_VERSION = '1.0.0'