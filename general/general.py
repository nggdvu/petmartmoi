from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from utils.tools import MessageType

general_blueprint = Blueprint('general', __name__, template_folder='templates', static_folder='static', static_url_path='/assets')

@general_blueprint.route('/', methods=["POST", "GET"])
def index():
    from models import products, Platform, User, Orders
    
    products_hero_section = products.query.filter_by(name='Pate cho chó nước sốt vị thịt bò PEDIGREE Pouch Beef').first()
    products_best_seller = products.query.order_by(products.purchase_number).limit(10).all()
    products_by_price = products.query.order_by(products.price).all()
    products_recommended = []
    pc = Platform.query.filter_by(platform_name='chó cảnh').first()
    curr_user = User.query.filter_by(id=2).first()
    session['current_user'] = []
    cart_length = 0
    if curr_user:
        orders = Orders.query.filter_by(customer_id = curr_user.id).all()
        cart_length = len(orders)
        session['subtotal'] = 0
        session['cart'] = []
        for order in orders:
            products_order_obj = {
                'image': order.products.image,
                'name': order.products.name,
                'price': order.products.price
            }
            session['cart'].append(products_order_obj)
            session['subtotal'] += order.products.price
            
        user_obj = {
            'username': curr_user.username,
            'name': curr_user.name,
            'budget': curr_user.budget
        }
        session['current_user'] = user_obj

    session['cart_length'] = cart_length

    for products in products_by_price:
        if pc in products.platforms_of_products:
            products_recommended.append(products)
            
    return render_template('general/index.html', products_best_seller=products_best_seller, products_recommended=products_recommended, products_hero_section=products_hero_section)