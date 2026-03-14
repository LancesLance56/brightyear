import os
from pathlib import Path
from urllib.parse import quote

from flask import Flask, render_template, request, redirect
import db


def create_app(test_config=None):
    BASE_DIR = Path(__file__).resolve().parent.parent

    app = Flask(__name__, instance_relative_config=True)

    default_db_path = BASE_DIR.joinpath('instance', 'src.sqlite')
    database_path = os.environ.get('DATABASE', str(default_db_path))

    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        DATABASE=database_path,
        UPLOAD_FOLDER=os.path.join(app.root_path, 'static', 'uploads'),
        ALLOWED_EXTENSIONS={'png', 'jpg', 'jpeg', 'gif'},
        MAX_CONTENT_LENGTH=16 * 1024 * 1024  # 16MB limit
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # Ensure necessary directories exist
    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    from src.db import get_db

    @app.route('/')
    def index():
        conn = get_db()
        products = conn.execute(
            'SELECT id, name, description, image_url, price, category FROM product'
        ).fetchall()
        return render_template("home.html", products=products)

    @app.route('/catalog')
    def catalog():
        conn = get_db()
        products = conn.execute(
            'SELECT id, name, description, image_url, price, category FROM product'
        ).fetchall()
        return render_template("catalog.html", products=products)

    @app.route('/contact', methods=['GET', 'POST'])
    def contact_page():
        if request.method == 'POST':
            name = request.form.get('name')
            project_type = request.form.get('project_type')

            ref_data = quote(f"Name:{name}|Project:{project_type}")

            messenger_url = f"https://www.messenger.com/t/veneerphilippines?ref={ref_data}"

            return redirect(messenger_url)

        return render_template('contact.html')

    @app.route('/map')
    def map_page():
        return render_template('map.html')

    # Initialize DB and Blueprints
    db.init_app(app)

    # Use relative imports if these are within the same package
    import auth
    import admin
    app.register_blueprint(auth.bp)
    app.register_blueprint(admin.bp)

    return app
