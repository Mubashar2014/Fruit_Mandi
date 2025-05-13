from flask import Blueprint, request, render_template, redirect, url_for, flash
from app import db
from app.models.users import Product

products_bp = Blueprint('products', __name__)

@products_bp.route('/')
def product_list():
    products = Product.query.all()
    return render_template('products/list.html', products=products)

@products_bp.route('/add', methods=['GET', 'POST'])
def add_product():
    products = Product.query.all()
    if request.method == 'POST':
        name = request.form['name']
        commission = request.form['commission']
        mazdoori = request.form['mazdoori']
        market_fees = request.form['market_fees']
        rent = request.form['rent']
        munshiyaana = request.form['munshiyaana']

        new_product = Product(name=name, commission=commission, mazdoori=mazdoori,
                              market_fees=market_fees, rent=rent, munshiyaana=munshiyaana)
        db.session.add(new_product)
        db.session.commit()
        flash('Product added successfully', 'success')
        return redirect(url_for('products.product_list'))

    return render_template('products/add_products.html', products = products)
