from flask import Flask, render_template, request, redirect, url_for
import os
import copy

app = Flask(__name__)

app.config['FLASK_TITLE'] = "Jayson Franco "

# --- IN-MEMORY DATA STRUCTURES (Students will modify this area) ---
# Phase 1: A simple Python List to store contacts
# Class Node: Represents a node in a linked list

class Node:
    def __init__(self, data):
        self.data = data # Data stored in the node
        self.next = None # Pointer to the next node

# Class LinkedList: Represents the linked list data structure
class LinkedList:
    def __init__(self):
        self.head = None # Head of the linked list

    # Method to insert a new node at the end of the linked list
    def append(self, data):
        new_node = Node(data)

        if not self.head: # If the list is empty, set the new node as the head
            self.head = new_node
            return
        
        last = self.head        # start at the head
        while last.next:        # traverse to the end of the list
            last = last.next    # move to the next node
        last.next = new_node    # link the last node to the new node

    # Method to iterate through the linked list
    def __iter__(self):          # allows iteration over the linked list
        current = self.head      # start at the head   
        while current:           # traverse until the end of the list
            yield current.data       # yield the data of the current node
            current = current.next  # move to the next node

    # New as of 4 Feb 2026: Remove a contact by name (DELETE)
    # Returns the removed contact if found, otherwise None
    def remove_by_name(self, name): 
        if not name or not self.head:
            return None

        current = self.head
        previous = None

        while current:
            if current.data["name"].lower() == name.lower():
                if previous is None:
                    self.head = current.next
                else:
                    previous.next = current.next
                return current.data
            
            previous = current
            current = current.next

        return None
    
    # Clone the linked list (deep copy) so Undo snapshots don't get mutated
    def clone(self):
        new_list = LinkedList()
        current = self.head

        while current:
            new_list.append(copy.deepcopy(current.data))
            current = current.next
        return new_list                                                             
        
    # Create a Stack class for Push/Pop, LIFO, Undo functionality
class Stack:
    def __init__(self):
        self.data = []

    def push(self, item):
        self.data.append(item)

    def pop(self):
        if not self.is_empty():
            return self.data.pop()
        return None
    
    def peek(self):
        if not self.is_empty():
            return self.data[-1]
        return None

    def is_empty(self):
        return len(self.data) == 0
    
    def size(self):
        return len(self.data)


contacts = LinkedList()

contacts.append({"name": "Alice", "email": "alice@example.com"})
contacts.append({"name": "Bob", "email": "bob@example.com"})
contacts.append({"name": "Charlie", "email": "charlie@example.com"})
contacts.append({"name": "Diana", "email": "diana@example.com"})

# Three Stacks required by session 6 / Stacks.txt style
actions_stack = Stack()  # Stack to track actions for Undo functionality
undo_add_stack = Stack()  # Stack to track undone additions
deleted_stack = Stack()    # Stack to track deleted contacts for Redo functionality

#contacts = [{"name": "Alice", "email": "alice@example.com"},
#            {"name": "Bob", "email": "bob@example.com"},
#           {"name": "Charlie", "email": "charlie@example.com"},
#           {"name": "Diana", "email": "diana@example.com"}]

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
                         title=app.config['FLASK_TITLE'],
                         can_undo=(not actions_stack.is_empty())
                         )


@app.route('/add', methods=['POST'])
def add_contact():
    """
    Endpoint to add a new contact.
    Students will update this to insert into their Data Structure.
    Add:
    1. push snapshot before add
    2. append new contact
    3. push action "A"dd to actions_stack
    """
    name = request.form.get('name')
    email = request.form.get('email')

    if not name or not email:
        return redirect(url_for('index'))
    
    # 1. snapshot before add
    undo_add_stack.push(contacts.clone())
    # 2. add new contact
    contacts.append({"name": name, "email": email})
    # 3. push action "A"dd to actions_stack
    actions_stack.push("A")

    return redirect(url_for('index'))
    
    # Phase 1 Logic: Append to list
    #Contacts.append({"name": name, "email": email})
    #actions_stack.push(("add", contacts.copy())  

@app.route('/delete', methods=['POST'])
def delete_contact():
    """
    Endpoint to delete a contact by name.
    Students will implement this to delete from their Data Structure.
    Delete:
    1. push snapshot before delete
    2. remove contact
    3. push action "D"elete to actions_stack
    """
    name = request.form.get('name')
    removed = contacts.remove_by_name(name)

    if removed:
        
        deleted_stack.push(removed)
        actions_stack.push("D")

    return redirect(url_for('index'))

@app.route('/undo', methods=['POST'])
def undo_action():
   
    global contacts
    
    last_action = actions_stack.pop()

    if last_action is None:
        return redirect(url_for('index'))

    if last_action == "A":
        # Undo Add: Restore from undo_add_stack
        previous_snapshot = undo_add_stack.pop()

        if previous_snapshot is not None:
            contacts = previous_snapshot
            if previous_snapshot is not None:
                contacts = previous_snapshot

    elif last_action == "D":
        # Undo Delete: Re-add the last deleted contact
        deleted = deleted_stack.pop()

        if deleted is not None  :
            contacts.append(deleted)

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
