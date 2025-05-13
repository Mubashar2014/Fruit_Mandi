from datetime import datetime

from flask import Blueprint, request, render_template, redirect, url_for, flash
from sqlalchemy import func

from app import db
from app.models.users import Product, Supplier, Customer, bill_customer_details, Bill, CustomerBillRecord

soorh_bp = Blueprint('soorh', __name__)

from flask import request, jsonify


@soorh_bp.route('/view_ghutka', methods=['GET', 'POST'])
def view_ghutka():
    date_str = request.args.get('date')
    if not date_str:
        date_str = datetime.today().strftime('%Y-%m-%d')

    # Fetch all bills for the selected date
    bills = Bill.query.filter_by(created_at=date_str).all()

    # Fetch customer-wise grouped data (name, sum of neg and rupeh)
    customers_summary = db.session.query(
        CustomerBillRecord.customer_name,
        func.sum(CustomerBillRecord.neg).label("total_neg"),
        func.sum(CustomerBillRecord.ropeh).label("total_rupeh")
    ).join(Bill).filter(
        Bill.created_at == date_str
    ).group_by(CustomerBillRecord.customer_name).all()

    naqdi_kela_kharbozeh = db.session.query(
        func.sum(CustomerBillRecord.total).label("total_sum")
    ).filter(
        CustomerBillRecord.date_created == date_str,
        CustomerBillRecord.customer_name == "نقدی",
        CustomerBillRecord.product.in_(["کیلا", "خربوزہ"])
    ).scalar()

    naqdi_other = db.session.query(
        func.sum(CustomerBillRecord.total).label("total_sum")
    ).filter(
        CustomerBillRecord.date_created == date_str,
        CustomerBillRecord.customer_name == "نقدی",
        CustomerBillRecord.product.notin_(["کیلا", "خربوزہ"])
    ).scalar()

    other_kela_kharbozeh = db.session.query(
        func.sum(CustomerBillRecord.total).label("total_sum")
    ).filter(
        CustomerBillRecord.date_created == date_str,
        CustomerBillRecord.customer_name != "نقدی",
        CustomerBillRecord.product.in_(["کیلا", "خربوزہ"])
    ).scalar()

    other_other = db.session.query(
        func.sum(CustomerBillRecord.total).label("total_sum")
    ).filter(
        CustomerBillRecord.date_created == date_str,
        CustomerBillRecord.customer_name != "نقدی",
        CustomerBillRecord.product.notin_(["کیلا", "خربوزہ"])
    ).scalar()

    chungi_sum = db.session.query(
        func.sum(Bill.chungi).label("total_sum")
    ).filter(
        Bill.created_at == date_str
    ).scalar()
    print(chungi_sum)

    return render_template(
        'soorh/soorh.html',
        bills=bills,
        selected_date=date_str,
        customers_summary=customers_summary,
        naqdi_kela_kharbozeh=naqdi_kela_kharbozeh,
        naqdi_other=naqdi_other,
        other_kela_kharbozeh=other_kela_kharbozeh,
        other_other=other_other,
        chungi_sum=chungi_sum
    )


@soorh_bp.route('/delete_bill/<int:bill_id>', methods=['POST'])
def delete_bill(bill_id):
    bill = Bill.query.get_or_404(bill_id)
    CustomerBillRecord.query.filter_by(bill_id=bill.id).delete()
    db.session.delete(bill)
    db.session.commit()
    flash("بل کامیابی سے حذف کر دیا گیا۔", "success")
    return redirect(url_for('soorh.view_ghutka', date=bill.date_entered))


@soorh_bp.route('/edit_bill/<int:bill_id>')
def edit_bill(bill_id):
    bill = Bill.query.get_or_404(bill_id)
    records = CustomerBillRecord.query.filter_by(bill_id=bill_id).all()
    customers = Customer.query.all()
    suppliers = Supplier.query.all()
    products = Product.query.all()

    return render_template(
        'ghutka/ghutka.html',
        bill=bill,
        records=records,
        customers=customers,
        suppliers=suppliers,
        products=products,
        editing=True  # flag to show we are in edit mode
    )


@soorh_bp.route('/print_receipt/<int:bill_id>')
def print_receipt(bill_id):
    bill = db.session.query(Bill).filter_by(id=bill_id).first()
    if not bill:
        return "Bill not found", 404

    customers = db.session.query(CustomerBillRecord).filter_by(bill_id=bill_id).all()

    return render_template('soorh/print_receipt.html', bill=bill, customers=customers)
