# app.py
import os
from flask import Flask
from config import Config
from flask_cors import CORS
from database.db import init_db
from routes.health import health_bp
from routes.logs import logs_bp
from routes.results import results_bp
from routes.analytics import analytics_bp
from routes.predict import predict_bp
from routes.predict_csv import predict_csv_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    init_db()

    app.register_blueprint(health_bp)
    app.register_blueprint(logs_bp, url_prefix="/api")
    app.register_blueprint(predict_bp, url_prefix="/api")
    app.register_blueprint(predict_csv_bp, url_prefix="/api")
    app.register_blueprint(analytics_bp, url_prefix="/api")
    app.register_blueprint(results_bp, url_prefix="/api")


    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
