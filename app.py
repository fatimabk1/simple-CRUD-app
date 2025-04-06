from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

from database import setup_db, Contact, db

def create_app():
    app = Flask(__name__, template_folder='./templates')
    CORS(app) 
    return app

app = create_app()
setup_db(app)

@app.route('/', methods=['GET'])
def serve_frontend():
    return send_from_directory('templates', 'index.html')

@app.route('/contacts/', methods=['GET'])
def get_contacts():
    contacts = Contact.query.all()
    contacts_dict = [contact.to_dict() for contact in contacts]
    print("contact count: ", len(contacts_dict))
    return jsonify(contacts_dict), 200

@app.route('/contacts/', methods=['POST'])
def add_contact():
    data = request.json
    new_contact = Contact(**data)

    db.session.add(new_contact)

    try:
        db.session.commit()
        return jsonify(new_contact.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    

@app.route('/contacts/<uuid:contact_id>', methods=['PUT'])
def update_contact(contact_id):
    data = request.json
    contact = Contact.query.get(str(contact_id))

    if not contact:
        return jsonify({"error": "Contact to update not found"}), 404

    field = data.get("field")
    value = data.get("value")

    if not field or value is None:
        return jsonify({"error": "Updated field cannot be empty"}), 400

    if not hasattr(contact, field): 
        return jsonify({"error": f"Field '{field}' not found"}), 400

    setattr(contact, field, value)

    try:
        db.session.commit()
        return jsonify({field: getattr(contact, field)}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route('/contacts/<uuid:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    contact = Contact.query.get(str(contact_id))
    if contact:
        db.session.delete(contact)
        try:
            db.session.commit()
            return jsonify({"message": "Contact deleted"}), 204
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Contact not found"}), 404
    

if __name__ == "__main__":
    port = os.environ.get('PORT', 5000)  # Default to 5000 if PORT is not set
    app.run(debug=True, host='0.0.0.0', port=int(port))