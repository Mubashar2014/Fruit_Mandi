from flask import Blueprint, request, render_template, redirect, url_for, flash, jsonify
from app import db
from app.models.users import Product, Supplier, Customer, bill_customer_details, Bill, CustomerBillRecord

ghutka_bp = Blueprint('ghutka', __name__)



@ghutka_bp.route('/add', methods=['POST'])
def ghutka_add():
    try:
        data = request.get_json()

        bill_data = data.get('bill')
        records = data.get('records', [])

        # 1. Create and save the Bill
        bill = Bill(
            supplier_id=bill_data.get('supplier_id'),
            maarkah=bill_data.get('maarkah'),
            car_number=bill_data.get('car_number'),
            total_nagg=bill_data.get('total_nagg'),
            kham_bikri=bill_data.get('kham_bikri'),
            rent_laari=bill_data.get('rent_laari'),
            mazdoori=bill_data.get('mazdoori'),
            daag=bill_data.get('daag'),
            munshiyana=bill_data.get('munshiyana'),
            market_fees=bill_data.get('market_fees'),
            chungi=bill_data.get('chungi'),
            amanat=bill_data.get('amanat'),
            custom=bill_data.get('custom'),
            extra_rent=bill_data.get('extra_rent'),
            commission=bill_data.get('commission'),
            pukhta_bikri=bill_data.get('pukhta_bikri'),
            created_at=bill_data.get('created_at'),
            date_entered=bill_data.get('date_entered'),
            date_out=bill_data.get('date_out'),
            wasool=bill_data.get('wasool'),
            total_amount=bill_data.get('total_amount'),
            nagad = bill_data.get('nagad'),

        )

        db.session.add(bill)
        db.session.commit()
        bill_expense = bill.calculate_expense()


        bill.expense = bill_expense
        db.session.commit()

        # 2. Save each related record with this bill's ID
        for rec in records:
            record = CustomerBillRecord(
                bill_id=bill.id,  # Foreign key reference
                product=rec.get('product'),
                neg=rec.get('neg'),
                ropeh=rec.get('ropeh'),
                total=rec.get('total'),
                chungi=rec.get('chongi'),
                customer_name=rec.get('customerName'),
                date_created=bill_data.get('created_at'),

            )
            db.session.add(record)

        db.session.commit()  # Commit all records at once

        return jsonify({"success": True}), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


# Render the form if it's a GET request
@ghutka_bp.route('/add', methods=['GET'])
def ghutka_add_form():
    customers = Customer.query.all()
    suppliers = Supplier.query.all()
    products = Product.query.all()
    return render_template('ghutka/ghutka.html', customers=customers, suppliers=suppliers, products=products)

@ghutka_bp.route('/edit_bill/<int:bill_id>')
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


@ghutka_bp.route('/update_bill', methods=['POST'])
def update_bill():
    data = request.get_json()

    bill_data = data.get('bill')
    records = data.get('records', [])

    bill_id = bill_data.get('id')
    bill = Bill.query.get_or_404(bill_id)

    # Update fields
    bill.total_nagg = bill_data.get('total_nagg')
    bill.kham_bikri = bill_data.get('kham_bikri')
    bill.rent_laari = bill_data.get('rent_laari')
    bill.mazdoori = bill_data.get('mazdoori')
    bill.daag = bill_data.get('daag')
    bill.munshiyana = bill_data.get('munshiyana')
    bill.market_fees = bill_data.get('market_fees')
    bill.chungi = bill_data.get('chungi')
    bill.amanat = bill_data.get('amanat')
    bill.custom = bill_data.get('custom')
    bill.extra_rent = bill_data.get('extra_rent')
    bill.commission = bill_data.get('commission')
    bill.pukhta_bikri = bill_data.get('pukhta_bikri')
    bill.nagad = bill_data.get('nagad')
    bill.total_amount = bill_data.get('total_amount')
    bill.created_at = bill_data.get('created_at')

    # Optional: Update expense if needed
    bill.expense = (
            int(bill.nagad or 0) + int(bill.commission or 0) + int(bill.mazdoori or 0) +
            int(bill.market_fees or 0) + int(bill.rent_laari or 0) + int(bill.munshiyana or 0) +
            int(bill.daag or 0) + int(bill.chungi or 0) + int(bill.amanat or 0) +
            int(bill.custom or 0) + int(bill.extra_rent or 0)
    )

    # Optional: Delete and replace old records
    CustomerBillRecord.query.filter_by(bill_id=bill_id).delete()

    for rec in records:
        new_record = CustomerBillRecord(
            bill_id=bill.id,  # Foreign key reference
            product=rec.get('product'),
            neg=rec.get('neg'),
            ropeh=rec.get('ropeh'),
            total=rec.get('total'),
            chungi=rec.get('chongi'),
            customer_name=rec.get('customerName'),
            date_created= bill_data.get('created_at'),
        )
        db.session.add(new_record)

    db.session.commit()

    return jsonify({"success": True})
