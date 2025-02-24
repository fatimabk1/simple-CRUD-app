document.addEventListener("DOMContentLoaded", function() {
    console.log("Loading initial HTML");
    
    // load contacts after inital HTML load
    fetch('/contacts/')
        .then(response => response.json())
        .then(data => updateContactList(data))
        .catch(error => console.error('Error fetching contacts:', error));

    // listener to submit POST request
    document.getElementById("new-contact-form").addEventListener("submit", function(event) {
        event.preventDefault();
        const formData = new FormData(event.target);
        const data = Object.fromEntries(formData.entries());

        fetch('/contacts/', {
            method: "POST",
            body: JSON.stringify(data),
            headers: {
                "Content-Type": "application/json"
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
            addContact(data);
            } else {
                console.log("Error adding new contact:", data.error);
            }
            event.target.reset();
        })
        .catch(error => console.log("Error adding new contact: ", error));
    });
});

// set initial contact list
function updateContactList(contacts) {
    console.log("Updating contact list with", contacts.length, "contacts." );

    const contactList = document.getElementById('contact-list');
    contactList.innerHTML = '';

    contacts.forEach(contact => {
        const tr = createRow(contact);
        contactList.appendChild(tr);
    });
}

function addContact(contact) {
    console.log("Adding contact to list");
    const contactList = document.getElementById('contact-list');

    const tr = createRow(contact);
    contactList.appendChild(tr);
}

function updateContact(contactId, updatedField) {
    console.log("Updating edited contact")
    fetch(`/contacts/${contactId}`, {
        method: 'PUT',
        body: JSON.stringify(updatedField),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to update contact');
        }
        return response.json();
    })
    .then(data => {
        console.log('Contact updated successfully:', data);
    })
    .catch(error => console.error('Error updating contact:', error));
}

function deleteContact(contactId) {
    console.log("Deleting contact with ID:", contactId);
    fetch(`/contacts/${contactId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.ok) {
            // Remove the row from the table
            const row = document.getElementById(contactId);
            row.parentNode.removeChild(row);
            console.log("Contact deleted successfully");
        } else {
            console.error("Failed to delete contact:", response.statusText);
        }
    })
    .catch(error => console.error("Error deleting contact:", error));
}

function createRow(contact) {
    const tr = document.createElement('tr');
    tr.setAttribute("id", contact.id);

    tr.appendChild(createEditableCell(contact.first, 'first'));
    tr.appendChild(createEditableCell(contact.last, 'last'));
    tr.appendChild(createEditableCell(contact.phone, 'phone'));
    tr.appendChild(createEditableCell(contact.email, 'email'));
    tr.appendChild(createEditableCell(contact.address, 'address'));

    // delete button
    const deleteButtonTd = document.createElement('td');
    const deleteButton = document.createElement('button');
    deleteButton.textContent = 'Delete';
    deleteButton.className = 'btn btn-danger';
    deleteButton.addEventListener('click', function() {
        deleteContact(contact.id);
    });
    deleteButtonTd.appendChild(deleteButton);
    tr.appendChild(deleteButtonTd);

    return tr;
}

function createEditableCell(value, fieldName) {
    const td = document.createElement('td');
    const input = document.createElement('input');
    input.type = 'text';
    input.value = value;

    // grab initial value
    input.addEventListener('focus', function() {
        input.setAttribute('data-initial-value', input.value);
    });

    input.addEventListener('blur', function() {
        const tr = input.closest('tr');
        const contactId = tr.getAttribute("id");

        if (!contactId) {
            console.error("Error: No contact ID found for row.");
            return;
        }

        const updatedField = {
            field: fieldName,
            value: input.value
        };

        // don't sent update if the user didn't actually update (clicked on then clicked off)
        const initialValue = input.getAttribute('data-initial-value');
        if (initialValue === input.value) { return; }

        updateContact(contactId, updatedField);
    });

    td.appendChild(input);
    return td;
}