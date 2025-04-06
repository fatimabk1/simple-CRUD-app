import uuid, os

from flask_sqlalchemy import SQLAlchemy
import pyodbc

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Access securely stored secrets for database connection string
credential = DefaultAzureCredential()
vault_url = "https://contacts-key-vault.vault.azure.net/"
client = SecretClient(vault_url=vault_url, credential=credential)

secret = "db-connection-string"
db_connection_string = client.get_secret(secret).value

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
    app.config['SQLALCHEMY_DATABASE_URI'] = db_connection_string
    # (
    #     f"mssql+pyodbc://{db_user}:{db_password}@"
    #     f"{db_host}:{db_port}/{db_name}?"
    #     "driver=FreeTDS&Encrypt=yes&TrustServerCertificate=no&TDS_Version=8.0"
    # )
    # db_connection_string = "mssql+pyodbc://azureuser:$25azurepass@fk-contacts-sql-server.database.windows.net:1433/contacts-db?driver=FreeTDS&Encrypt=yes&TrustServerCertificate=no&TDS_Version=8.0"


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
