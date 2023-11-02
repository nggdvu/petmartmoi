#MODELS ARE TABLES IN DATABASE
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    hash_password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.Enum('customer', 'admin'), nullable=False, default='customer')
    name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(50), nullable=True, unique=True)
    budget = db.Column(db.Integer, nullable=False, default=5000000)
    # One to Many Relationship (For customer)
    orders = db.relationship('Orders', backref='customer', lazy=True)
    purchases = db.relationship('Purchases', backref='customer', lazy=True)

    def __repr__(self):
        return f'User {self.username}'
    
    def can_purchase(self, total_orders):
        return self.budget >= total_orders
    
    def purchase_item(self, total):
        self.budget -= total
        db.session.commit()

genre_products = db.Table('genre_products',
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), primary_key=True),
    db.Column('products_id', db.Integer, db.ForeignKey('products.id'), primary_key=True)
)

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String(30), nullable=False, unique=True)
    # Many to Many Relationship
    products_of_genre = db.relationship(
        'products', 
        secondary=genre_products, 
        lazy='subquery', 
        backref=db.backref('genres_of_products', lazy=True)
        )

    def __repr__(self):
        return f'Genre {self.genre_name}'


class brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand_name = db.Column(db.String(50), nullable=False, unique=True)
    # One to Many Relationship
    products = db.relationship('products', backref='brand', lazy=True)

    def __repr__(self):
        return f'brand {self.brand_name}'

platform_products = db.Table('platform_products',
    db.Column('platform_id', db.Integer, db.ForeignKey('platform.id'), primary_key=True),
    db.Column('products_id', db.Integer, db.ForeignKey('products.id'), primary_key=True)
)

class Platform(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    platform_name = db.Column(db.String(50), nullable=False, unique=True)
    # Many to Many Relationship
    products_on_platform = db.relationship(
        'products', 
        secondary=platform_products, 
        lazy='subquery', 
        backref=db.backref('platforms_of_products', lazy=True)
        )

    def __repr__(self):
        return f'Platform {self.platform_name}'


class products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    description = db.Column(db.String(1024), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(1024), nullable=True, default='https://www.uri.edu/wordpress/wp-content/uploads/home/sites/7/500x333.png')
    purchase_number = db.Column(db.Integer, nullable=True, default=0)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=False)
    # One to Many Relationship
    order = db.relationship('Orders', backref='products', lazy=True)
    purchases = db.relationship('Purchases', backref='products', lazy=True)
    # Many to Many Relationship with: Platform (use 'platforms_of_products'), Genre (use 'genres_of_products')

    def __repr__(self):
        return f'products {self.id} {self.name} {self.description} {self.price} {self.image} {self.purchase_number} {self.brand_id} {self.order} {self.purchases}'

    def purchased_success(self):
        self.purchase_number += 1
        db.session.commit()
        
class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_of_order = db.Column(db.DateTime, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    products_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    # Many to One Relationship with: Customer (use 'customer'), products (use 'products')

    def __repr__(self):
        return f'Order {self.id}: products {self.products_id} - Customer: {self.customer_id}'
    

class Purchases(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_of_purchase = db.Column(db.DateTime, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    products_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    # Many to One Relationship with: Customer (use 'customer'), products (use 'products')

    def __repr__(self):
        return f'Purchase {self.id}'