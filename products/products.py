from flask import Blueprint, render_template, request, flash
from utils.tools import MessageType

products_blueprint = Blueprint('products', __name__, template_folder='templates',  static_folder='static', static_url_path='/static')

@products_blueprint.route('/')
def index():
    from models import products, Platform, Genre

    page = request.args.get('page', 1, type = int)

    # fetch products from db
    products_query = products.query.paginate(page = page, per_page= 9)

    platforms_query = Platform.query.all()
    genres_query = Genre.query.all()

    renderItem = render_template('components/Item.html', products_query = products_query)
    renderSideBar = render_template('components/SideBar.html', platforms_query = platforms_query, genres_query = genres_query)
    renderDropdown = render_template('components/Dropdown.html')
    renderSearch = render_template('components/Search.html')
    renderPagination = render_template('components/Pagination.html', pages = products_query.iter_pages(left_edge=1, right_edge=1, left_current=1, right_current=2), current_page = products_query.page)

    return render_template('products.html', Item = renderItem, SideBar = renderSideBar, Dropdown = renderDropdown, Search = renderSearch, Pagination = renderPagination)

@products_blueprint.route('')
def filter_products():
    from models import Platform, Genre

    platform_text = request.args.get('platform', '', type = str)
    genre_text = request.args.get('genre', '', type = str)

    # fetch products from db
    platforms_query = Platform.query.all()
    genres_query = Genre.query.all()

    platform_query = Platform.query.filter_by(platform_name = platform_text).first()
    genre_query = Genre.query.filter_by(genre_name = genre_text).first()
    products_query = []
    if platform_query:
        products_query = platform_query.products_on_platform
    if genre_query:
        products_query = genre_query.products_of_genre
        

    renderItem = render_template('components/Item.html', products_query = products_query)
    renderSideBar = render_template('components/SideBar.html', platforms_query = platforms_query, genres_query = genres_query)
    renderDropdown = render_template('components/Dropdown.html')
    renderSearch = render_template('components/Search.html')

    return render_template('products.html', Item = renderItem, SideBar = renderSideBar, Dropdown = renderDropdown, Search = renderSearch)


@products_blueprint.route('/sort?=<sort_by>',)
def sort_products(sort_by):
    from models import products, Platform, Genre

    platforms_query = Platform.query.all()
    genres_query = Genre.query.all()
    
    match sort_by:
        case "name_desc":
            products_query = products.query.order_by(products.name.desc()).all()
            option_value = "Xếp từ Z - A"
        case "price_asc":
            products_query = products.query.order_by(products.price.asc()).all()
            option_value = "Giá thấp nhất"
        case "price_desc":
            products_query = products.query.order_by(products.price.desc()).all()
            option_value = "Giá cao nhất"
        case _:
            products_query = products.query.order_by(products.name.asc()).all()
            option_value = "Xếp từ A - Z"


    renderItem = render_template('components/Item.html', products_query = products_query)
    renderSideBar = render_template('components/SideBar.html', platforms_query = platforms_query, genres_query = genres_query)
    renderDropdown = render_template('components/Dropdown.html' , option_value = option_value)
    renderSearch = render_template('components/Search.html')

    return render_template('products.html', Item = renderItem, SideBar = renderSideBar, Dropdown = renderDropdown, Search = renderSearch)

@products_blueprint.route('/<product_id>')
def product_detail(product_id):
    from models import products

    products_query = products.query.filter_by(id = product_id).first()
    renderBreadcrumbs = render_template('components/Breadcrumbs.html', product_name = products_query.name)

    return render_template('product-detail.html', Breadcrumbs = renderBreadcrumbs, products_query = products_query, platforms_of_products = products_query.platforms_of_products, genres_of_products = products_query.genres_of_products, brand = products_query.brand, products_id=product_id)

@products_blueprint.route('', methods = ['POST'])
def handle_search():
    from models import products
    from models import products, Platform, Genre

    search_text = request.args.get('search', '', type = str)

    platforms_query = Platform.query.all()
    genres_query = Genre.query.all()

    products_query = products.query.filter(products.name.like(f'%{search_text}%')).all()

    renderItem = render_template('components/Item.html', products_query = products_query)
    renderSideBar = render_template('components/SideBar.html', platforms_query = platforms_query, genres_query = genres_query)
    renderDropdown = render_template('components/Dropdown.html')
    renderSearch = render_template('components/Search.html')

    return render_template('products.html', Item = renderItem, SideBar = renderSideBar, Dropdown = renderDropdown, Search = renderSearch, search_text = search_text)

@products_blueprint.route('/best-sellers')
def best_sellers():
    from models import products, Platform, Genre

    pageTitle = 'BÁN CHẠY NHẤT'
    products_best_seller = products.query.order_by(products.purchase_number).limit(10).all()
    platforms_query = Platform.query.all()
    genres_query = Genre.query.all()

    platforms_query = Platform.query.all()
    genres_query = Genre.query.all()

    renderItem = render_template('components/Item.html', products_query = products_best_seller)
    renderSideBar = render_template('components/SideBar.html', platforms_query = platforms_query, genres_query = genres_query)
    renderDropdown = render_template('components/Dropdown.html')
    renderSearch = render_template('components/Search.html')

    return render_template('products.html', Item = renderItem, SideBar = renderSideBar, Dropdown = renderDropdown, Search = renderSearch, pageTitle=pageTitle)

@products_blueprint.route('/featured-and-recommended')
def featured_recommended():
    from models import products, Platform, Genre

    pageTitle = 'DỊCH VỤ'
    platforms_query = Platform.query.all()
    genres_query = Genre.query.all()

    platforms_query = Platform.query.all()
    genres_query = Genre.query.all()

    products_by_price = products.query.order_by(products.price).all()
    products_recommended = []
    pc = Platform.query.filter_by(platform_name='PC').first()

    for products in products_by_price:
        if pc in products.platforms_of_products:
            products_recommended.append(products)

    renderItem = render_template('components/Item.html', products_query = products_recommended)
    renderSideBar = render_template('components/SideBar.html', platforms_query = platforms_query, genres_query = genres_query)
    renderDropdown = render_template('components/Dropdown.html')
    renderSearch = render_template('components/Search.html')

    return render_template('products.html', Item = renderItem, SideBar = renderSideBar, Dropdown = renderDropdown, Search = renderSearch, pageTitle=pageTitle)