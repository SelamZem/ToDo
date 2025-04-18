from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config

db = SQLAlchemy() 
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.secret_key = "abc"
    db.init_app(app)  
    migrate.init_app(app, db)

    from .routes import routes
    app.register_blueprint(routes)

    return app
