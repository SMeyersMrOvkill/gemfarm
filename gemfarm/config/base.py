import os
import logging

class Config:
    """Base configuration."""
    # Flask
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'default-secret-key')
    
    # API Keys
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY', '')
    
    # WebSocket settings
    CORS_ALLOWED_ORIGINS = "*"
    
    # Rate limiting
    MAX_REQUESTS_PER_MINUTE = 10
    
    # Logging
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_LEVEL = logging.INFO
    
    @classmethod
    def init_app(cls, app):
        """Initialize application configuration."""
        # Set up logging
        logging.basicConfig(
            level=app.config['LOG_LEVEL'],
            format=app.config['LOG_FORMAT']
        )
