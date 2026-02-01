from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

app.config['FLASK_TITLE'] = "Jayson Franco "

# --- IN-MEMORY DATA STRUCTURES (Students will modify this area) ---
# Phase 1: A simple Python List to store contacts
# Class Node: Represents a node in a linked list

contacts = LinkedList"name": "Alice", "email": "alice@example.com"},
            {"name": "Bob", "email": "bob@example.com"},
            {"name": "Charlie", "email": "charlie@example.com"},
            {"name": "Diana", "email": "diana@example.com"})

# Searches for a contact by name, ignoring case.
# Returns the contact's name if found, otherwise returns None.
def find_contact_by_name(name):
    if not name:
        return None
    for contact in contacts:
        if contact["name"].lower() == name.lower():
            return contact
    return None

# --- ROUTES ---


@app.route('/search')
def search_contact():
    query = request.args.get('query')
    result = find_contact_by_name(query)
    if result:
        return f"Contact found: {result}"
    else:
        return "Contact not found."

@app.route('/')
def index():
    # Change the Flask HTML Title to Jayson Franco
    # Modify the title in the config above
    """
    Displays the main page.
    Eventually, students will pass their Linked List or Tree data here.
    """
    return render_template('index.html', 
                         contacts=contacts, 
                         title=app.config['FLASK_TITLE'])

@app.route('/add', methods=['POST'])
def add_contact():
    """
    Endpoint to add a new contact.
    Students will update this to insert into their Data Structure.
    """
    name = request.form.get('name')
    email = request.form.get('email')

    new_name = request.form['name']
    
    # Phase 1 Logic: Append to list
    contacts.append({"name": new_name, "email": email})

    return redirect(url_for('index'))

# --- DATABASE CONNECTIVITY (For later phases) ---
# Placeholders for students to fill in during Sessions 5 and 27
def get_postgres_connection():
    pass

def get_mssql_connection():
    pass

if __name__ == '__main__':
    # Run the Flask app on port 5000, accessible externally
    app.run(host='0.0.0.0', port=5000, debug=True)
