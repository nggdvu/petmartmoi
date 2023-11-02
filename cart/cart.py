from flask import Blueprint, redirect, render_template, request, session, flash
from models import products, Orders, User, Purchases
from datetime import datetime
from app import db
from utils.tools import MessageType

cart_blueprint = Blueprint('cart', __name__, template_folder='templates', static_folder='static', static_url_path='/static')

@cart_blueprint.route('/', methods=['POST', 'GET'])
def index():
    curr_user = User.query.filter_by(id=2).first()
    orders = Orders.query.filter_by(customer_id = curr_user.id).all()
    products_in_cart = []
    subtotal = 0
    discount = 0
    taxes = 0
    if orders:
        for order in orders:
            products = products.query.filter_by(id=order.products_id).first()
            products_in_cart.append(products)
            subtotal += products.price
        taxes = subtotal * 5 / 100
    total = subtotal + taxes + discount
    if request.method == 'POST':
        if products_in_cart:
            if curr_user.can_purchase(total):
                for products in products_in_cart:
                    new_purchase = Purchases(
                        customer_id=curr_user.id, 
                        products_id=products.id, 
                        date_of_purchase=datetime.now()
                    )
                    db.session.add(new_purchase)
                    products.purchased_success()
                curr_user.purchase_item(total)
                for order in orders:
                    db.session.delete(order)
                db.session.commit()
                session['cart_length'] = 0
                session['current_user']['budget'] = curr_user.budget
                flash(f'Purchase successfully!', category=MessageType['SUCCESS'].value)
            else:
                flash(f'Your balance is not enough for this purchasing!', category=MessageType['ERROR'].value)
        else:
            flash(f'Your cart is empty, please go back and shopping :D', category=MessageType['ERROR'].value)
        return redirect(request.referrer)
    return render_template('cart/cart.html', cart=products_in_cart, subtotal=subtotal, discount=discount, taxes=taxes, total=total)

@cart_blueprint.route('/add', methods=["POST"])
def cart_add():
    products_id = int(request.form['product_id'])
    curr_user = User.query.filter_by(id=2).first()
    order_exist = Orders.query.filter_by(customer_id=curr_user.id, products_id=products_id).first()
    purchase_exist = Purchases.query.filter_by(customer_id=curr_user.id,  products_id=products_id).first()
    if request.method == "POST":
        found = False
        if order_exist:
            found = True
            flash(f'This products was already in your cart!', category=MessageType['ERROR'].value)
        elif purchase_exist:
            found = True
            flash(f'You already bought this products!', category=MessageType['ERROR'].value)
        if not found:
            newOrder = Orders(
                date_of_order = datetime.now(),
                customer_id = curr_user.id,
                products_id = products_id
            )
            db.session.add(newOrder)
            db.session.commit()
            order_add = Orders.query.filter_by(products_id=newOrder.products_id).first()
            products_order_obj = {
                'image': order_add.products.image,
                'name': order_add.products.name,
                'price': order_add.products.price
            }
            session['cart'].append(products_order_obj)
            session['subtotal'] += order_add.products.price
            session['cart_length'] = len(session['cart'])
            flash(f'Added to cart successfully!', category=MessageType['SUCCESS'].value)    

    return redirect(request.referrer)

@cart_blueprint.route('/remove/<products_id>', methods=['POST'])
def cart_remove(products_id):
    curr_user = User.query.filter_by(id=2).first()
    deleted_order = Orders.query.filter_by(customer_id=curr_user.id, products_id=products_id).first()

    if request.method == 'POST':
        if deleted_order:
            products_order_obj = {
                'image': deleted_order.products.image,
                'name': deleted_order.products.name,
                'price': deleted_order.products.price
            }
            session['cart'].remove(products_order_obj)
            session['subtotal'] -= deleted_order.products.price
            db.session.delete(deleted_order)
        db.session.commit()
        
        session['cart_length'] = len(session['cart'])
    return redirect(request.referrer)