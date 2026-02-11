from collections import deque
from flask import Flask, render_template, request, redirect, url_for
import os
import copy

app = Flask(__name__)
app.config['FLASK_TITLE'] = "Jayson Franco "

# Queue class for recent activity log, FIFO
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

# Data + Index (Hash Table) **Session 8**
contacts = LinkedList() 

contacts.append({"name": "Alice", "email": "alice@example.com"})
contacts.append({"name": "Bob", "email": "bob@example.com"})
contacts.append({"name": "Charlie", "email": "charlie@example.com"})
contacts.append({"name": "Diana", "email": "diana@example.com"})

# Hash Table for indexing contacts by name (for O(1) search) **Session 8**
contacts_index = {}

def index_contacts():
    contacts_index.clear()
    for contact in contacts:
        contacts_index[contact["name"].lower()] = contact

index_contacts()  # Initial indexing of contacts

# Undo/Redo: Three Stacks required by session 6 / Stacks.txt style
actions_stack = Stack()      # Stack to track actions for Undo functionality
undo_add_stack = Stack()     # Stack to track undone additions
deleted_stack = Stack()      # Stack to track deleted contacts for Redo functionality

# Track what was added so Undo(add) can enqueue the correct redo
added_contacts_stack = Stack()  # Stack to track added contacts for Undo functionality

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

# Search (O(1) using Hash Table) **Session 8**
def find_contact_by_name(name): 
    if not name:
        return None
    return contacts_index.get(name.lower()) # O(1) lookup using dictionary

# --- ROUTES ---

@app.route('/search')
def search_contact():
    query = request.args.get('query', '') # ****Double Check this is the correct way to get query parameter in Flask****
    result = find_contact_by_name(query)

    log_activity(f"Search: {query} -> {'Found' if result else 'Not Found'}")

    if result:
        return f"Contact found: {result['name']} ({result['email']})"
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

    # 2. Perform the add operation (append to linked list and update hash table index)
    new_contact = {"name": name, "email": email}
    contacts.append(new_contact)

    # Remember exactly what was added
    added_contacts_stack.push(copy.deepcopy(new_contact))

    # 3. push action "A"dd to actions_stackand record action in activity log
    actions_stack.push("A")

    # Rebuild hash index after modification
    index_contacts()

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
    
    if not name:
        return redirect(url_for('index'))
    
    clear_redo_queue() # Session 7: Clear redo queue when a new action is performed after an undo, to maintain correct redo state

    removed = contacts.remove_by_name(name)

    if removed:
        deleted_stack.push(removed)
        actions_stack.push("D")

        index_contacts() # Rebuild hash index after modification

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
        last_added_contact = added_contacts_stack.pop() # Get the last added contact for redo tracking

        if previous_snapshot is not None:
            contacts = previous_snapshot

            if last_added_contact is not None:
                redo_queue.append(("A", copy.deepcopy(last_added_contact)))  # Store snapshot after undo for redo

            index_contacts() # Rebuild hash index after modification
            log_activity(f"Undo: Removed added contact: {last_added_contact['name']}") #Session 7 Activity Log

    elif last_action == "D":
        # Undo Delete: Restore the last deleted contact
        deleted = deleted_stack.pop()

        if deleted is not None  :
            contacts.append(deleted)

            redo_queue.append(("D", copy.deepcopy(deleted)))  # Store deleted contact for redo
           
            index_contacts() # Rebuild hash index after modification
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

    action, contacts_snapshot = redo_queue.popleft() # *****Double check this line

    if action == "A":
        # Redo Add: Restore from snapshot
        if contacts_snapshot is None:
            clear_redo_queue()  # Clear redo queue if snapshot is invalid
            log_activity("Redo failed: Invalid snapshot for add action") #Session 7 Activity Log
        contacts = contacts_snapshot
        actions_stack.push("A")

        index_contacts() # Rebuild hash index after modification
        log_activity(f"Redo: restored last add action: {contacts_snapshot['name']}") #Session 7 Activity Log

    elif action == "D":
        if contacts_snapshot is None:
            clear_redo_queue()  # Clear redo queue if snapshot is invalid
            log_activity("Redo failed: Invalid snapshot for delete action") #Session 7 Activity Log 
            if os.remove is not None:
                contacts.append(contacts_snapshot)
                actions_stack.push("D")

                index_contacts() # Rebuild hash index after modification
                log_activity(f"Redo: restored last delete action: {contacts_snapshot['name']}") #Session 7 Activity Log
            else:
                log_activity("Redo failed: No contact to restore for delete action") #Session 7 Activity Log    
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
