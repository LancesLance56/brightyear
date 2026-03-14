import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from src.auth import login_required  # We will add this decorator next
from src.db import get_db

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/')
@login_required
def index():
    db = get_db()
    products = db.execute('SELECT * FROM product ORDER BY id DESC').fetchall()
    return render_template('admin/index.html', products=products)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        category = request.form.get('category')

        file = request.files.get('image_file')
        filename = None

        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        if not name:
            flash('Name is required.')
        elif not description:
            flash('Description is required.')
        else:
            db = get_db()
            db.execute(
                'INSERT INTO product (name, description, image_url, price, category) VALUES (?, ?, ?, ?, ?)',
                (name, description, filename, price, category)
            )
            db.commit()
            flash(f"Successfully added {name}!")
            return redirect(url_for('admin.index'))

    return render_template('admin/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    db = get_db()
    product = db.execute('SELECT * FROM product WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')  # Add this
        category = request.form.get('category')  # Add this

        file = request.files.get('image_file')
        filename = product['image_url']  # Default to the existing image

        # If a new file was actually uploaded, save it
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        if not name:
            flash('Name is required.')
        else:
            db.execute(
                'UPDATE product SET name = ?, description = ?, image_url = ?, price = ?, category = ? WHERE id = ?',
                (name, description, filename, price, category, id)
            )
            db.commit()
            return redirect(url_for('admin.index'))

    return render_template('admin/edit.html', product=product)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    db = get_db()
    db.execute('DELETE FROM product WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('admin.index'))


@bp.route('/<int:id>/edit', methods=('GET', 'POST'))
@login_required
def edit(id):
    db = get_db()
    # Fetch the specific product or return a 404 if it doesn't exist
    product = db.execute(
        'SELECT * FROM product WHERE id = ?', (id,)
    ).fetchone()

    if product is None:
        abort(404, f"Product id {id} doesn't exist.")

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        image_url = request.form['image_url']
        price = request.form['price']
        category = request.form['category']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)
        else:
            db.execute(
                'UPDATE product SET name = ?, description = ?, image_url = ?'
                ' WHERE id = ?',
                (name, description, image_url, id, price, category)
            )
            db.commit()
            flash(f"Successfully updated {name}!")
            return redirect(url_for('admin.index'))

    return render_template('admin/edit.html', product=product)


def allowed_file(filename, allowed_extensions):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in allowed_extensions
