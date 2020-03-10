
from flask import Blueprint, render_template
from store.logic.forms import ProductForm
from store.models.logic import Product, Brand, Category

logic= Blueprint('logic', __name__)

@logic.route('/dashboard/products', methods=['POST', 'GET'])
def products():
    form= ProductForm()
    return render_template('logic/products.html', form=form)

@logic.route('/dashboard/orders')
def orders():
    return render_template('logic/orders.html')