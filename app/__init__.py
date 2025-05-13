from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('configuration.Config')

    db.init_app(app)
    Migrate(app, db)

    # Register Blueprints
    from app.blueprints.auth.routes import auth_bp
    from app.blueprints.products.routes import products_bp
    from app.blueprints.customers.routes import customers_bp
    from app.blueprints.suppliers.routes import suppliers_bp
    from app.blueprints.ghutka.routes import ghutka_bp
    from app.blueprints.soorh.routes import soorh_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(suppliers_bp, url_prefix='/suppliers')
    app.register_blueprint(products_bp, url_prefix='/products')
    app.register_blueprint(ghutka_bp, url_prefix='/ghutka')
    app.register_blueprint(soorh_bp, url_prefix='/soorh')

    @app.route('/')
    def index():
        return redirect('/auth')

    return app
