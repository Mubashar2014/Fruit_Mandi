from app import db


class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False, unique=True)
    supplier_type = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200))
    main_supplier = db.Column(db.String(200))
    balance = db.Column(db.String(200))

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    commission = db.Column(db.String(20), nullable=False)
    mazdoori = db.Column(db.String(20), nullable=False)
    market_fees = db.Column(db.String(20), nullable=False)
    rent = db.Column(db.String(20), nullable=False)
    munshiyaana = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# Junction Table: This will store the relationship between Bill and Customer along with neg and total
bill_customer_details = db.Table('bill_customer_details',
    db.Column('bill_id', db.Integer, db.ForeignKey('bill.id'), primary_key=True),
    db.Column('customer_id', db.Integer, db.ForeignKey('customer.id'), primary_key=True),
    db.Column('neg', db.Integer, nullable=False),
    db.Column('total', db.Integer, nullable=False)

)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False, unique=True)
    customer_type = db.Column(db.String(20), nullable=False)
    other_balance = db.Column(db.String(20))
    banana_melon_balance = db.Column(db.String(20))
    address = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    bills = db.relationship('Bill', secondary=bill_customer_details, back_populates='customers')


class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())
    total_amount = db.Column(db.Float, nullable=False)


class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())
    total_amount = db.Column(db.Float, nullable=False)


class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    maarkah = db.Column(db.String(20))
    car_number = db.Column(db.String(20))
    total_nagg = db.Column(db.Integer, nullable=False)
    kham_bikri = db.Column(db.Integer, nullable=False)
    rent_laari = db.Column(db.Integer)
    mazdoori = db.Column(db.Integer)
    daag = db.Column(db.Integer)
    munshiyana = db.Column(db.Integer)
    market_fees = db.Column(db.Integer)
    chungi = db.Column(db.Integer)
    amanat = db.Column(db.Integer)
    custom = db.Column(db.Integer)
    extra_rent = db.Column(db.Integer)
    commission = db.Column(db.Integer)
    pukhta_bikri = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    date_entered = db.Column(db.DateTime)
    nagad = db.Column(db.Integer, default=0)
    date_out = db.Column(db.DateTime)
    wasool = db.Column(db.Integer)
    expense = db.Column(db.Integer)
    total_amount = db.Column(db.Float, nullable=False)

    # Relationship with Customer through the junction table
    customers = db.relationship('Customer', secondary=bill_customer_details, back_populates='bills')

    supplier = db.relationship('Supplier', backref='bills')

    def calculate_expense(self):
        return (self.nagad + self.commission + self.mazdoori + self.market_fees +
                self.rent_laari + self.munshiyana + self.daag + self.chungi +
                self.amanat + self.custom + self.extra_rent)

class CustomerBillRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bill_id = db.Column(db.Integer, db.ForeignKey('bill.id'), nullable=False)  # Foreign key to bill table
    product = db.Column(db.String(100))
    neg = db.Column(db.String(50))
    ropeh = db.Column(db.String(50))
    total = db.Column(db.String(50))
    chungi = db.Column(db.String(50))
    customer_name = db.Column(db.String(100))
    date_created = db.Column(db.DateTime)


    biller = db.relationship('Bill', backref='records')

# Now the junction table for the Bill model is ready for saving and querying customers' neg and total values.