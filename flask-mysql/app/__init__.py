from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Kolawole1997@localhost:3306/flask_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .route import routes        
    app.register_blueprint(routes)

    with app.app_context():
        from .authors_models import Author
        db.create_all()

    return app