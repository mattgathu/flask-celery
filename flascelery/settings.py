"""
Application config / settings

"""
import os

# ============================================================================
# Celery config
# ============================================================================
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# ============================================================================
# Flask-Mail configuration
# ============================================================================
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_SSL = False
MAIL_USE_TLS = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSOWRD')
MAIL_DEFAULT_SENDER = 'flask@example.com'

# ============================================================================
# EOF
# ============================================================================
