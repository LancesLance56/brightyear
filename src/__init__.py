import os

from flask import Flask
from flask import render_template

from src.db import get_db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'src.sqlite')
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    os.makedirs(app.instance_path, exist_ok=True)

    UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit uploads to 16MB

    # Ensure the upload folder exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    @app.route('/')
    def index():
        db = get_db()
        products = db.execute(
            'SELECT id, name, description, image_url, price, category FROM product'
        ).fetchall()
        return render_template("home.html", products=products)

    @app.route('/catalog')
    def catalog():
        db = get_db()
        products = db.execute(
            'SELECT id, name, description, image_url, price, category FROM product'
        ).fetchall()
        return render_template("catalog.html", products=products)

    @app.route('/contact')
    def contact():
        return render_template('contact.html')

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import admin
    app.register_blueprint(admin.bp)

    return app
