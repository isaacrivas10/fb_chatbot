
from store import db, admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.model import BaseModelView
from datetime import datetime

class Product(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    product_identifier= db.Column(db.String(10), nullable=False)
    product_name= db.Column(db.String(40), nullable=False)
    product_description= db.Column(db.Text, nullable=False)
    pictures= db.Column(db.PickleType, nullable=False)
    unit_price= db.Column(db.Float, nullable=False)
    product_available= db.Column(db.Boolean, default=True)
    delivery= db.Column(db.String(20), nullable=False)
    brand_id= db.Column(db.Integer, db.ForeignKey('brand.id'))
    category_id= db.Column(db.Integer, db.ForeignKey('category.id'))
    discount_available= db.Column(db.Boolean, default=False)
    discount_percentage= db.Column(db.Float, nullable=True)
    pub_date = db.Column(db.DateTime, index=True,
        default=datetime.utcnow)

    def save_imgs(self, img_list):
        self.pictures= img_list

    def __repr__(self):
        return f"Product('{self.product_identifier}',\
        '{self.product_name}',\
        '{self.brand}')"
    
class Brand(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(20), nullable=False)
    products= db.relationship('Product', backref='brand', lazy=True)

    def __repr__(self):
        return f"Brand('{self.name}')"
    
class Category(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(20), nullable=False)
    products= db.relationship('Product', backref='category', lazy=True)

    def __repr__(self):
        return f"Category('{self.name}')"

class Order(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'))
    order_number= db.Column(db.Integer, nullable=False)
    items= db.relationship('OrderItem', backref='order', lazy=True)
    paid= db.Column(db.Boolean, default=False)
    fulfilled= db.Column(db.Boolean, default=False)
    cancelled= db.Column(db.Boolean, default=False)
    err_msg= db.Column(db.String(60), nullable=True)
    err_log= db.Column(db.PickleType, nullable=True)
    date_placed = db.Column(db.DateTime, index=True,
        default=datetime.utcnow)

class OrderItem(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    product_id= db.Column(db.Integer, db.ForeignKey('product.id'))
    order_id= db.Column(db.Integer, db.ForeignKey('order.id'))
    quantity= db.Column(db.Integer, nullable=False)

class PSNAccounts(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    email= db.Column(db.String(120), nullable=False)
    password= db.Column(db.String(60), nullable=False)
    account_holder= db.Column(db.String(60), nullable=False)
    games= db.Column(db.String(60), nullable=False)

def get_name_tuple(db):
    objs= db.query.all()
    choices= list()
    
    for obj in objs:
        choices.append(
            (obj, obj.name)
        )
    
    return choices


class LogicView(ModelView):
    create_modal= True
    edit_modal= True

class ProductView(LogicView):
    column_searchable_list= ['brand_id']

class CategoryView(LogicView):
    form_ajax_refs = {
        'products': {
            'fields': ['category']
        }
    }

class OrderView(LogicView):
    column_searchable_list= ['order_number']

admin.add_views(
    ProductView(Product, db.session, name='Products', category='Store'),
    LogicView(Brand, db.session, name='Brands', category='Store'),
    CategoryView(Category, db.session, name='Categories', category='Store'),
    OrderView(Order, db.session, name='Orders')
)