import uuid

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Contact(db.Model):
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    first = db.Column(db.String)
    last = db.Column(db.String)
    phone = db.Column(db.String)
    email = db.Column(db.String)
    address = db.Column(db.String)

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
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
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
