import os
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'e7d30731f0ed276800ddc4245f15cc3ee7631ba3463ecbae0d61fd18dd6380d7'
    # Format: mysql+pymysql://<username>:<password>@<host>/<database_name>
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://root:afaqmub321@localhost/fruit_mandi_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
