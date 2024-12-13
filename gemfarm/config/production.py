from .base import Config
import logging

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    LOG_LEVEL = logging.INFO
    
    @classmethod
    def init_app(cls, app):
        super().init_app(app)
        
        # Production-specific initialization
        file_handler = logging.FileHandler('production.log')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter(Config.LOG_FORMAT))
        
        app.logger.addHandler(file_handler)
