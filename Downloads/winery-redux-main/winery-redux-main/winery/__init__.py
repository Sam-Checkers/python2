from flask import Flask, request, render_template, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from winery.config import Config

# Add this monkey patch for CockroachDB compatibility
from sqlalchemy.dialects.postgresql.base import PGDialect
from sqlalchemy import text

# Store the original method
original_get_server_version_info = PGDialect._get_server_version_info

# Define a patched method
def _patched_get_server_version_info(self, connection):
    try:
        # Use text() to create an executable SQL expression
        version_string = connection.scalar(text("SELECT version()"))
        if version_string and 'cockroach' in version_string.lower():
            # Return a PostgreSQL version that SQLAlchemy can handle
            return (9, 5, 0)
        else:
            return original_get_server_version_info(self, connection)
    except Exception:
        # Fallback to a compatible version if there's any error
        return (9, 5, 0)

# Apply the patch
PGDialect._get_server_version_info = _patched_get_server_version_info

# Continue with the rest of your initialization
from winery.models import db as root_db, login_manager, ma

app = Flask(__name__)
CORS(app)
bcrypt = Bcrypt(app)
app.config.from_object(Config)
root_db.init_app(app)
login_manager.init_app(app)
ma.init_app(app)
migrate = Migrate(app, root_db)

from winery import routes

if __name__ == '__main__':
    app.run(debug=True)