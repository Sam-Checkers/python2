import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

# Path to certificate relative to this file
cert_path = os.path.join(basedir, 'certs', 'root.crt')

class Config:
    FLASK_APP = os.getenv('FLASK_APP')
    FLASK_ENV = os.getenv('FLASK_ENV')
    SECRET_KEY = os.environ.get('SECRET_KEY') or '12345'
    
    # Use the DATABASE_URI from .env
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Check if certificate file exists
    if os.path.exists(cert_path):
        # Use certificate verification
        SQLALCHEMY_ENGINE_OPTIONS = {
            'connect_args': {
                'application_name': 'winery-download',
                'sslmode': 'verify-full',
                'sslrootcert': cert_path
            }
        }
    else:
        # Fall back to require mode
        SQLALCHEMY_ENGINE_OPTIONS = {
            'connect_args': {
                'application_name': 'winery-download',
                'sslmode': 'require'
            }
        }