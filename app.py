# app.py
from flask import Flask
from config import Config
from database.db import init_db
from routes.features import features_bp
from routes.health import health_bp
from routes.logs import logs_bp
from routes.results import results_bp
from routes.analytics import analytics_bp



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize database
    init_db()

    # Register blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(logs_bp, url_prefix="/api")
    app.register_blueprint(results_bp, url_prefix="/api")
    app.register_blueprint(features_bp, url_prefix="/api")
    app.register_blueprint(analytics_bp, url_prefix="/api")
    


    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
