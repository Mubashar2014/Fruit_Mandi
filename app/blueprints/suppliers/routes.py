from flask import Blueprint, request, render_template, redirect, url_for, flash
from app import db
from app.models.users import Supplier

suppliers_bp = Blueprint('suppliers', __name__)

@suppliers_bp.route('/')
def supplier_list():
    suppliers = Supplier.query.all()
    return render_template('suppliers/list.html', suppliers=suppliers)

@suppliers_bp.route('/add', methods=['GET', 'POST'])
def add_supplier():
    suppliers = Supplier.query.all()
    if request.method == 'POST':
        name = request.form['name']
        number = request.form['number']
        supplier_type = request.form.get('supplier_type')
        address = request.form.get('address')
        balance = request.form.get('balance')

        if not request.form['main_supplier']:
            main_supplier = None
        else:
            main_supplier = request.form['main_supplier']

        new_supplier = Supplier(name=name, phone=number, supplier_type=supplier_type,
                                address=address, balance=balance, main_supplier=main_supplier)
        db.session.add(new_supplier)
        db.session.commit()
        flash('Supplier added successfully', 'success')
        return redirect(url_for('suppliers.supplier_list'))

    return render_template('suppliers/add_suppliers.html', suppliers = suppliers)
