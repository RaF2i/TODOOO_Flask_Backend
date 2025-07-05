# __init__.py

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize SQLAlchemy
db = SQLAlchemy()

def create_app():
    """
    Application factory function. Creates and configures the Flask app.
    """
    app = Flask(__name__)
    
    # Configure the app
    app.config['SECRET_KEY'] = os.environ.get('JWT_SECRET')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    
    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    with app.app_context():
        # Import and register blueprints
        from . import routes
        app.register_blueprint(routes.api_bp)
        
        # You can create the database tables if they don't exist
        # db.create_all() 

    return app