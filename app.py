import os
import logging
from flask import Flask, render_template
from database import db, init_db

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def create_app():
    # Initialize Flask app
    app = Flask(__name__)
    
    # Configure app
    app.config.update(
        SECRET_KEY=os.environ.get("FLASK_SECRET_KEY", "fashion-feature-extraction-key")
    )
    
    # Initialize database
    init_db(app)
    
    # Import routes after db initialization to avoid circular imports
    with app.app_context():
        from routes import init_routes
        init_routes(app)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {error}")
        db.session.rollback()
        return render_template('errors/500.html'), 500
        
    return app

# Create the application instance
app = create_app()