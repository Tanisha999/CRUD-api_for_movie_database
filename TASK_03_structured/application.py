from flask import Flask
from extensions import db
from routes.director_routes import director
from routes.movies_routes import movie
from routes.cast_routes import cast
import os

def create_app():
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'task_03.sqlite3')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()
        print("Database tables created.")

    app.register_blueprint(director)
    app.register_blueprint(movie)
    app.register_blueprint(cast)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)