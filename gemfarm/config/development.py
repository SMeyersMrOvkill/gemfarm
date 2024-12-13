from .base import Config
import logging

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    LOG_LEVEL = logging.DEBUG
    
    @classmethod
    def init_app(cls, app):
        super().init_app(app)
        
        # Development-specific initialization
        app.logger.debug('Running in development mode')
