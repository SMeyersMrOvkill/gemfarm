import os
from flask import Flask
from flask_socketio import SocketIO
from gemfarm.config import config

socketio = SocketIO()

def create_app(config_name='default'):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    config_class = config[config_name]
    app.config.from_object(config_class)
    config_class.init_app(app)
    
    # Initialize extensions
    socketio.init_app(app, cors_allowed_origins=app.config['CORS_ALLOWED_ORIGINS'])
    
    # Register blueprints
    from gemfarm.game import bp as game_bp
    from gemfarm.chat import bp as chat_bp
    
    app.register_blueprint(game_bp)
    app.register_blueprint(chat_bp)
    
    return app

def __main__():
    create_app()