# This file contains the application factory.

from flask import Flask, g
from flask_cors import CORS
import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

def get_db():
    """
    Opens a new database connection if there is none yet for the
    current application context.
    """
    if 'db' not in g:
        g.db = psycopg2.connect(os.environ.get('DATABASE_URL'))
    return g.db

def close_db(e=None):
    """
    Closes the database connection at the end of the request.
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()

def create_app():
    """
    Application factory function. Creates and configures the Flask app.
    """
    app = Flask(__name__)
    
    # Set secret key for the app
    app.config['SECRET_KEY'] = os.environ.get('JWT_SECRET')
    
    # Enable CORS to allow your Next.js frontend (e.g., from http://localhost:3000)
    # to make requests to this Flask backend.
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register the function to close the database connection when the app context is torn down
    app.teardown_appcontext(close_db)

    # Import and register the routes from routes.py
    from . import routes
    app.register_blueprint(routes.api_bp)

    return app
