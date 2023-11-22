from flask import Blueprint, render_template, request, redirect, flash
from utils.tools import MessageType
from app import db

admin_blueprint = Blueprint('admin', __name__, template_folder='templates')

@admin_blueprint.route('/auth/login')
def admin_login():

    return render_template('admin-login.html')

@admin_blueprint.route('/')
def management():
    from models import products, brand, Genre, Platform

    # fetch products from db
    products_query = products.query.all()
    brands_query = brand.query.all()
    genres_query = Genre.query.all()
    platforms_query = Platform.query.all()

    render_modal_create_product = render_template('components/ModalCreateProduct.html', brands_query = brands_query, genres_query = genres_query, platforms_query = platforms_query)
    render_search = render_template('components/SearchBar.html')

    return render_template('management.html', products_query = products_query, ModalCreateProduct = render_modal_create_product, Search = render_search)

@admin_blueprint.route('/search', methods = ['POST'])
def handle_search():
    from models import products, brand, Genre, Platform

    # fetch products from db
    brands_query = brand.query.all()
    genres_query = Genre.query.all()
    platforms_query = Platform.query.all()

    search_text = request.form['search_input']
    products_query = products.query.filter(products.name.like(f'%{search_text}%')).all()

    render_modal_create_product = render_template('components/ModalCreateProduct.html', brands_query = brands_query, genres_query = genres_query, platforms_query = platforms_query)
    render_search = render_template('components/SearchBar.html')

    return render_template('management.html', products_query = products_query, ModalCreateProduct = render_modal_create_product, Search = render_search)

@admin_blueprint.route('create-product', methods = ['POST'])
def create_product():
    from models import products, Genre, Platform

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        image = request.form['image_url']
        purchase_number = 0
        brand_id = request.form['brand']
        genres = request.form.getlist('genres')
        platforms = request.form.getlist('platforms')

        new_product = products(name = name, description = description, price = price, image = image,purchase_number = purchase_number ,brand_id = brand_id)
        new_product.genres_of_product = Genre.query.filter(Genre.id.in_(genres)).all()
        new_product.platforms_of_product = Platform.query.filter(Platform.id.in_(platforms)).all()

        try:
            db.session.add(new_product)
            db.session.commit()

            success_message = "Created successfully!"
            flash(f'{success_message}', category = MessageType['SUCCESS'].value)
        except:
            error_message = "Something went wrong! (POST: admin/create-product)"
            flash(f'Error: {error_message}', category = MessageType['ERROR'].value)

            db.session.rollback()
            
        finally:
            return redirect('/admin')

@admin_blueprint.route('edit-product/<product_id>', methods = ['GET', 'POST'])
def edit_product(product_id):
    from models import products, brand

    product_query = products.query.filter_by(id = product_id).first()
    brands_query = brand.query.all()

    if request.method == 'POST':
        if product_query:
            name = request.form['name']
            description = request.form['description']
            price = request.form['price']
            image = request.form['image_url']
            brand_id = request.form['brand']

            # Update the attributes of product_query
            product_query.name = name
            product_query.description = description
            product_query.price = price
            product_query.image = image
            product_query.brand_id = brand_id

            try:
                db.session.commit()

                success_message = "Updated successfully!"
                flash(f'{success_message}', category = MessageType['SUCCESS'].value)
            except:
                error_message = "Something went wrong! (POST: admin/edit-product)"
                flash(f'Error: {error_message}', category = MessageType['ERROR'].value)

                db.session.rollback()

    return render_template('edit-product.html', product_query = product_query, brands_query = brands_query, platforms_of_product = product_query.platforms_of_product, genres_of_product = product_query.genres_of_product, brand = product_query.brand)

@admin_blueprint.route('delete-product/<product_id>', methods = ['POST'])
def delete_product(product_id):
    from models import products

    product_query = products.query.filter_by(id = product_id).first()

    if request.method == 'POST':
        if product_query:
            try:
                db.session.delete(product_query)  # Delete the product
                db.session.commit()  # Commit the changes

                success_message = "Deleted successfully!"
                flash(f'{success_message}', category = MessageType['SUCCESS'].value)

            except Exception as e:
                db.session.rollback()
                error_message = "Something went wrong! (POST: admin/delete-product)"
                flash(f'Error: {error_message}', category = MessageType['ERROR'].value)

            finally:
                return redirect('/admin')
