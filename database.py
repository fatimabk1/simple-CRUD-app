import uuid, os

from flask_sqlalchemy import SQLAlchemy
import pyodbc

from azure.identity import ManagedIdentityCredential
from azure.keyvault.secrets import SecretClient

# Access securely stored secrets for database connection string
credential = ManagedIdentityCredential()
vault_url = "https://wse-keyvault.vault.azure.net/"
client = SecretClient(vault_url=vault_url, credential=credential)

db_user_secret = client.get_secret("DB_USER")
db_host_secret = client.get_secret("DB_HOST")
db_password_secret = client.get_secret("DB_PASSWORD")
db_port_secret = client.get_secret("DB_PORT")
db_name_secret = client.get_secret("DB_NAME")

db_user = db_user_secret.value
db_host = db_host_secret.value
db_password = db_password_secret.value
db_port = db_port_secret.value
db_name = db_name_secret.value

# Set up actual database
db = SQLAlchemy()

class Contact(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    first = db.Column(db.String(100))
    last = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(255))
    address = db.Column(db.String(255))

    def to_dict(self):
        return {
            'id': self.id,
            'first': self.first,
            'last': self.last,
            'phone': self.phone,
            'email': self.email,
            'address': self.address
        }

def setup_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mssql+pyodbc://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASSWORD')}@"
        f"{os.environ.get('DB_HOST')}:{os.environ.get('DB_PORT')}/{os.environ.get('DB_NAME')}?"
        "driver=FreeTDS&Encrypt=yes&TrustServerCertificate=no&TDS_Version=8.0"
    )
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
    db.init_app(app)
    with app.app_context():
        db.create_all()
        add_starter_data()
    return db

def add_starter_data():
    # only add starter data if we have an empty database
    if Contact.query.all():
        return

    starter_contacts = [
        {
            'first': 'Alice',
            'last': 'Apples',
            'phone': '123-456-7890',
            'email': 'alice.apples@example.com',
            'address': '123 Apples St, Apples, IL'
        },
        {
            'first': 'Bob',
            'last': 'Blueberries',
            'phone': '123-456-7890',
            'email': 'bob.blueberries@example.com',
            'address': '123 Blueberries St, Blueberries, IL'
        },
        {
            'first': 'Cathy',
            'last': 'Cranberries',
            'phone': '123-456-7890',
            'email': 'cathy.cranberries@example.com',
            'address': '123 Cranberries St, Cranberries, IL'
        },
        {
            'first': 'Dave',
            'last': 'Durian',
            'phone': '123-456-7890',
            'email': 'dave.durian@example.com',
            'address': '123 Durian St, Durian, IL'
        }
    ]

    for contact_data in starter_contacts:
        contact = Contact(
            first=contact_data['first'],
            last=contact_data['last'],
            phone=contact_data['phone'],
            email=contact_data['email'],
            address=contact_data['address']
        )
        db.session.add(contact)

    db.session.commit()
