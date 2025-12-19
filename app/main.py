from flask import Flask
from app.api.routes import api
from app.db.database import init_db

def create_app():
    app = Flask(__name__)

    init_db()  # initialize SQLite

    app.register_blueprint(api)

    @app.route("/")
    def home():
        return {"message": "Coin Tracker API is running 🚀"}

    return app
