from flask import Flask, render_template, request, redirect, url_for
import os
import copy
from datetime import datetime # Session 7: For timestamping activity logs
from collections import deque # Session 7: For efficient activity queue management


app = Flask(__name__)

app.config['FLASK_TITLE'] = "Jayson Franco "

# --- IN-MEMORY DATA STRUCTURES (Students will modify this area) ---
# Phase 1: A simple Python List to store contacts

# Create a Python class for a Queue data structure
# It should have enqueue, dequeue, is_empty, and size methods

class Queue:
    def __init__(self):
        self.data = []

    def enqueue(self, item):
        self.data.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.data.pop(0) # Its at pop(0) because its a queue, FIFO
        return None

    def is_empty(self):
        return len(self.data) == 0

    def size(self):
        return len(self.data)

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

# Redo stack is not implemented yet, but can be added similarly to the undo stacks if needed in future phases.
redo_queue = deque()  # Redo queue uses deque for efficient appends and pops from both ends, if we implement redo functionality later

# Queue for recent activity (FIFO)
activity_queue = Queue()

# Helper function to log messages to the activity queue
def log_activity(message):
    activity_queue.enqueue(message)
    # Limit the queue size to the most recent 10 activities
    while activity_queue.size() > 10:
        activity_queue.dequeue()

def clear_redo_queue():
    redo_queue.clear()  # Session 7: Clear redo queue when a new action is performed after an undo, to maintain correct redo state

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

    log_activity(f"Search: {query} -> {'Found' if result else 'Not Found'}")

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
                         can_undo=(not actions_stack.is_empty()),
                         can_redo=(len(redo_queue) > 0), # Session 7: Check if redo is possible
                         activities=activity_queue.data #Pass queue data to template
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
    
    clear_redo_queue() # Session 7: Clear redo queue when a new action is performed after an undo, to maintain correct redo state
    
    # 1. snapshot before add
    undo_add_stack.push(contacts.clone())
    # 2. add new contact
    contacts.append({"name": name, "email": email})
    # 3. push action "A"dd to actions_stack
    actions_stack.push("A")

    log_activity(f"Added contact: {name} ({email})") #Session 7 Activity Log

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

    clear_redo_queue() # Session 7: Clear redo queue when a new action is performed after an undo, to maintain correct redo state

    if removed:
        deleted_stack.push(removed)
        actions_stack.push("D")
        log_activity(f"Deleted contact: {name}") #Session 7 Activity Log
    else:
        log_activity(f"Delete failed, (not found): {name}") #Session 7 Activity Log

    return redirect(url_for('index'))

@app.route('/undo', methods=['POST'])
def undo_action():
   
    global contacts
    
    last_action = actions_stack.pop()

    if last_action is None:
        log_activity("Undo failed: No actions to undo") #Session 7 Activity Log
        return redirect(url_for('index'))

    if last_action == "A":
        # Undo Add: Restore from undo_add_stack
        previous_snapshot = undo_add_stack.pop()

        if previous_snapshot is not None:
            contacts = previous_snapshot
            redo_queue.append(("A", copy.deepcopy(contacts)))  # Optionally add to redo queue if implementing redo later
            log_activity("Undo: reverted last add action") #Session 7 Activity Log

    elif last_action == "D":
        # Un
        deleted = deleted_stack.pop()

        if deleted is not None  :
            contacts.append(deleted)
            redo_queue.append(("D", copy.deepcopy(contacts)))  # Optionally add to redo queue if implementing redo later
            log_activity(f"Undo: Restored deleted contact: {deleted['name']}") #Session 7 Activity Log
    return redirect(url_for('index'))

@app.route('/redo', methods=['POST'])
def redo_action():
    """
    Endpoint to redo the last undone action.
    """
    if not redo_queue:
        log_activity("Redo failed: No actions to redo") #Session 7 Activity Log
        return redirect(url_for('index'))

    action, contacts_snapshot = redo_queue.pop()

    if action == "A":
        # Redo Add: Restore from snapshot
        global contacts
        contacts = contacts_snapshot
        actions_stack.push("A")
        log_activity("Redo: restored last add action") #Session 7 Activity Log

    elif action == "D":
        removed = contacts.remove_by_name(contacts_snapshot.data[-1]["name"]) # Assuming the last contact in the snapshot is the one that was deleted
        if removed:
            actions_stack.push("D")
            log_activity(f"Redo: Re-deleted contact: {removed['name']}") #Session 7 Activity Log
        else:
            log_activity(f"Redo failed: Contact to delete not found: {contacts_snapshot.data[-1]['name']}") #Session 7 Activity Log 
            
    return redirect(url_for('index'))
                                                                                                    
    # Logic to add grade will go here
    log_activity("New grade added for student X") # Example log message
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
