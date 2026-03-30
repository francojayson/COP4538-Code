from collections import deque
# from Quick_Sort import partition
from flask import Flask, render_template, request, redirect, url_for
from TreeNode import TreeNode
# import os
import copy
import heapq    # For priority queue implementation in Session 14, can be used if we decide to implement a more efficient priority queue using heapq instead of the simple list-based one provided in PriorityQueue.py

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

# ----------TreeNode for Organizing Contacts by Category (Session 15)----------

# Create all the nodes
class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = []
    
    def add_child(self, child_node):
        self.children.append(child_node)

root = TreeNode("All Contacts")
work = TreeNode("Work")
personal = TreeNode("Personal")
engineers = TreeNode("Engineers")
hr = TreeNode("HR")

# Link the children to their parents
root.add_child(work)
root.add_child(personal)

work.add_child(engineers)
work.add_child(hr)

# ----------TreeNode for Organizing Contacts by Category (Session 15)----------

# ----------Homework 4: Category Tree BEGIN----------

class CategoryTreeNode:
    def __init__(self, name):
        self.name = name    
        
        self.children = {}  # Use a dictionary to store children for O(1) access by name

        self.contacts = []  # List to store contacts that belong to this category/subcategory/department/team
      
    def add_child(self, child_name):
        if child_name not in self.children:
            self.children[child_name] = CategoryTreeNode(child_name)
        return self.children[child_name]

class CategoryTree:
    def __init__(self):
        self.root = CategoryTreeNode("All Contacts")

    def clear(self):
        self.root = CategoryTreeNode("All Contacts")

    def insert_contact(self, contact):
        category = contact.get("category", "").strip() or "Uncategorized"
        department = contact.get("department", "").strip() or "General"
        team = contact.get("team", "").strip() or "General"

        category_node = self.root.add_child(CategoryTreeNode(category))
        department_node = category_node.add_child(CategoryTreeNode(department))
        team_node = department_node.add_child(CategoryTreeNode(team))

        team_node.contacts.append(contact)

    def to_nested_dict(self):
        result = {}

        for category_name, category_node in self.root.children.items():
            result[category_name] = {}
            for department_name, department_node in category_node.children.items():
                result[category_name][department_name] = {}
                for team_name, team_node in department_node.children.items():
                    result[category_name][department_name][team_name] = team_node.contacts

        return result
    
# ----------Homework 4: Category Tree END ----------

# ----------Data + Index (Hash Table) **Session 8** --------

contacts = LinkedList() 

#---------------Homework 4 Requirements Start----------------
# Adding more detailed contact information for Session 15 TreeNode organization and Session 13 ID search

contacts.append({
    "id": 1000, 
    "name": "Alice", 
    "email": "alice@example.com", 
    "category": "Work", 
    "subcategory": "Engineers",
    "department": "Engineering",
    "team": "Platform",
    "emergency_priority": 2
})

contacts.append({
    "id": 1001, 
    "name": "Bob", 
    "email": "bob@example.com", 
    "category": "Work", 
    "subcategory": "HR",
    "department": "Human Resources",
    "team": "Recruitment",
    "emergency_priority": 5
})

contacts.append({
    "id": 1002, 
    "name": "Charlie", 
    "email": "charlie@example.com", 
    "category": "Personal",
    "subcategory": "Friends",
    "department": "Family",
    "team": "Immediate Family",
    "emergency_priority": 1

})

contacts.append({
    "id": 1003, 
    "name": "Diana", 
    "email": "diana@example.com", 
    "category": "Work",
    "subcategory": "Engineers",
    "department": "Engineering",
    "team": "Security",
    "emergency_priority": 3
})

contacts.append({
    "id": 1005,
    "name": "Frank",
    "email": "frank@example.com",
    "category": "Work",
    "subcategory": "HR",
    "department": "HR",
    "team": "Payroll",
    "emergency_priority": 6
})
contacts.append({
    "id": 1006,
    "name": "Grace",
    "email": "grace@example.com",
    "category": "Personal",
    "subcategory": "",
    "department": "Friends",
    "team": "College Friends",
    "emergency_priority": 7
})
contacts.append({
    "id": 1007,
    "name": "Heidi",
    "email": "heidi@example.com",
    "category": "Personal",
    "subcategory": "",
    "department": "Friends",
    "team": "Neighborhood",
    "emergency_priority": 8
})
contacts.append({
    "id": 1008,
    "name": "Ivan",
    "email": "ivan@example.com",
    "category": "Personal",
    "subcategory": "",
    "department": "Family",
    "team": "Extended Family",
    "emergency_priority": 9
})
contacts.append({
    "id": 1009,
    "name": "Judy",
    "email": "judy@example.com",
    "category": "Personal",
    "subcategory": "",
    "department": "Friends",
    "team": "Travel Friends",
    "emergency_priority": 10
})
contacts.append({
    "id": 1010,
    "name": "Karl",
    "email": "karl@example.com",
    "category": "Personal",
    "subcategory": "",
    "department": "Friends",
    "team": "Gym Friends",
    "emergency_priority": 11
})
contacts.append({
    "id": 1011,
    "name": "Leo",
    "email": "leo@example.com",
    "category": "Personal",
    "subcategory": "",
    "department": "Friends",
    "team": "Gaming Friends",
    "emergency_priority": 12
})

next_id = 1012  # Initialize next ID for new contacts

# --------------Homework 4 Requirements End----------------


# ---------------Session 13 Start (ID Search)----------------

# Add a numeric ID to each contact for Session 13 search by ID functionality
# Add the Session 15 TreeNode organization to the initial contacts for demonstration, can be modified as needed
# contacts.append({"id": 1000, "name": "Alice", "email": "alice@example.com", "category": "Work", "subcategory": "Engineers"})
# contacts.append({"id": 1001, "name": "Bob", "email": "bob@example.com", "category": "Work", "subcategory": "HR"})
# contacts.append({"id": 1002, "name": "Charlie", "email": "charlie@example.com", "category": "Personal"})
# contacts.append({"id": 1003, "name": "Diana", "email": "diana@example.com", "category": "Work", "subcategory": "Engineers"})
#contacts.append({"id": 1004, "name": "Eve", "email": "eve@example.com", "category": "Personal"})
#contacts.append({"id": 1005, "name": "Frank", "email": "frank@example.com", "category": "Work", "subcategory": "HR"})
#contacts.append({"id": 1006, "name": "Grace", "email": "grace@example.com", "category": "Personal"})
#contacts.append({"id": 1007, "name": "Heidi", "email": "heidi@example.com", "category": "Personal"})
#contacts.append({"id": 1008, "name": "Ivan", "email": "ivan@example.com", "category": "Personal"})
#contacts.append({"id": 1009, "name": "Judy", "email": "judy@example.com", "category": "Personal"})
#contacts.append({"id": 1010, "name": "Karl", "email": "karl@example.com", "category": "Personal"})
#contacts.append({"id": 1011, "name": "Leo", "email": "leo@example.com", "category": "Personal"})
#next_id = 1012  # Initialize next ID for new contacts

# ---------------Session 13 End (ID Search)---------------------

# Hash Table for indexing contacts by name (for O(1) search) **Session 8**
contacts_index = {}

def index_contacts():
    contacts_index.clear()
    for contact in contacts:
        contacts_index[contact["name"].lower()] = contact

# Session 13: Fixes the issue of missing IDs for existing contacts if we decide to implement ID search in Session 13, can be called after any modification to contacts to ensure all have IDs
def ensure_ids():
    global next_id
    for c in contacts:
        if "id" not in c:
            c["id"] = next_id
            next_id += 1

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

# Ensures ID then build index for O(1) search by name, call this after any modification to contacts
ensure_ids() # Placeholder if we need to ensure IDs are assigned to existing contacts, can be implemented if needed
index_contacts()  # Initial indexing of contacts


# Search (O(1) using Hash Table) **Session 8**
def find_contact_by_name(name): 
    if not name:
        return None
    return contacts_index.get(name.lower()) # O(1) lookup using dictionary

# ------------------------- Session 13 Start "Binary Search" ----------------------------

# Binary search by ID for Session 13 search by ID functionality
def binary_search_by_id(contacts_list, target_id):
    low = 0
    high = len(contacts_list) - 1

    while low <= high:
        mid = (low + high) // 2
        guess_id = contacts_list[mid]["id"]

        if guess_id == target_id:
            return contacts_list[mid]
        elif guess_id < target_id:
            low = mid + 1
        else:
            high = mid - 1
    
    return None

# -------------------------- Session 13 End "Binary Search" ----------------------------


# --------------------Session 15: TreeNode Category Helper Function-----------------------

def get_contacts_by_category(category_name):
    # Returns all contacts in a specific category, case-insensitive match
    return [c for c in contacts if c.get("category", "").lower() == category_name.lower()]

def get_contacts_by_subcategory(category_name):
    # Returns all contacts in a specific subcategory, case-insensitive match
    return [c for c in contacts if c.get("subcategory", "").lower() == category_name.lower()]

def get_node_by_name(node, name):
    # Find a TreeNode by its data name, case-insensitive match
    if node.data.lower() == name.lower():
        return node
    for child in node.children:
        result = get_node_by_name(child, name)
        if result:
            return result
    return None

def get_all_contacts_under_node(node):
    # Returns all contacts under a specific node and its children, based on category and subcategory
    contacts_under_node = []
    # Get direct contacts for this node
    contacts_under_node.extend(get_contacts_by_category(node.data))

    # Also allow subcategory matches for child nodes (e.g. if node is "Work", also get contacts with subcategory "Work")
    contacts_under_node.extend(get_contacts_by_subcategory(node.data))

    # Get contacts from child nodes
    for child in node.children:
        contacts_under_node.extend(get_all_contacts_under_node(child))
    return contacts_under_node

def build_tree_from_contacts(contacts):
    tree_contacts = {
        "Work": [],
        "Personal": [], 
    }

    for contact in contacts:
        category = contact.get("category", "")
        if category in tree_contacts:
            tree_contacts[category].append(contact)

    return tree_contacts

#--------------------Session 15: TreeNode Category Helper Function-----------------------


# ----------Homework 4: Category Tree Helper Functions-----------------------

def normalize_contact_structure(contact):
    """
    Keeps backward compatibility with existing contacts while allowing for new category/subcategory structure.
    """
    if "department" not in contact or not contact.get("department"):
        subcategory = contact.get("subcategory", "").strip()
        if subcategory == "Engineers":
            contact["department"] = "Engineering"
            contact["team"] = contact.get("team", "") or "General"
        elif subcategory == "HR":
             contact["department"] = "HR"
             contact["team"] = contact.get("team", "") or "General"
        else:
            contact["department"] = "General"
            contact["team"] = subcategory or "General"
        
    if "team" not in contact or not contact.get("team"):
        contact["team"] = "General"

    if "emergency_priority" not in contact:
        contact["emergency_priority"] = 999

def get_category_path(contact):
    normalize_contact_structure(contact)
    category = contact.get("category", "").strip() or "Uncategorized"
    department = contact.get("department", "").strip() or "General"
    team = contact.get("team", "").strip() or "General"
    return f"{category} > {department} > {team}"


# --------------------Session 10 Quick Sort Implementation for sorting contacts by name "Phase 3 Homework"-----------------------

# Quick sort implementation from session 10 for sorting contacts by name.
def partition(arr, low, high):
    pivot = arr[high]["name"].lower()  # Choosing the last element as pivot
    
    i = low - 1  # Pointer for the smaller element
    for j in range(low, high):
        if arr[j]["name"].lower() <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]  # Swap

    arr[i + 1], arr[high] = arr[high], arr[i + 1]  # Swap the pivot element with the element at i+1
    return i + 1

def quick_sort(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)


# ---------------------------Session 9-------------------------------------------------------
# Add insertion sort function from Session 9 here, to be used in the /sort route
#def insertion_sort(items): # Insertion sort algorithm for session 9
#    for i in range(1, len(items)):
#        key = items[i]
#        j = i - 1
#        while j >= 0 and key["name"].lower() < items[j]["name"].lower():
#            items[j + 1] = items[j]
#            j -= 1
#        items[j + 1] = key
#    return items
# ---------------------------Session 9-------------------------------------------------------

# ---------------------------Session 16: Binary Search Tree (BST)-----------------------
# Changing contact to category for the BSTNode, since we are building a category tree in Session 16, but this can be modified as needed if we want to store contacts directly in the BST instead of using TreeNode
class CategoryBSTNode:
    def __init__(self, category):
        self.category = category
        self.left = None
        self.right = None

class CategoryBST:
    def __init__(self):
        self.root = None

    def insert(self, category):
        if not category:
            return
        
        category = category.strip() # Remove leading/trailing whitespace
        if category == "":
            return
        
        if self.root is None:
            self.root = CategoryBSTNode(category)
        else:
            self._insert_recursive(self.root, category)

    def _insert_recursive(self, node, category):
        # Change: left < node < right rule from Session 16
        if category.lower() < node.category.lower():
            if node.left is None:
                node.left = CategoryBSTNode(category)
            else:
                self._insert_recursive(node.left, category)
        elif category.lower() > node.category.lower():
            if node.right is None:
                node.right = CategoryBSTNode(category)
            else:
                self._insert_recursive(node.right, category)
        else:
            pass # Duplicate category, do nothing or handle as needed

    def inorder(self):
        categories = []
        self._inorder_recursive(self.root, categories)
        return categories
    
    def _inorder_recursive(self, node, categories):
        if node is not None:
            self._inorder_recursive(node.left, categories)
            categories.append(node.category)
            self._inorder_recursive(node.right, categories)

    def search(self, category):
        if not category:
            return False
        return self._search_recursive(self.root, category.strip().lower())

    def _search_recursive(self, node, category):
        if node is None:
            return False
        
        current = node.category.lower()

        if category == current:
            return True
        elif category.lower() < current:
            return self._search_recursive(node.left, category)
        else:
            return self._search_recursive(node.right, category)
        
# Global function to build a BST from the categories in the contacts, can be called in the index route to build the tree for display
category_bst = CategoryBST()

def rebuild_category_bst():
    global category_bst
    category_bst = CategoryBST()  # Reset the BST

    for contact in contacts:
        category_bst.insert(contact.get("category", ""))  # Insert category into BST, can be modified to insert subcategory or other fields as needed

# ----------------------------Session 16: Binary Search Tree (BST)-------------------------

# -------------------------Homework 4 Requirement Emergency Priority Queue (HEAP) BEGIN-------------------------

class EmergencyPriorityQueue:
    def __init__(self):
        self.heap = []

    def push(self, contact):
        normalize_contact_structure(contact)  # Ensure contact has emergency_priority and other fields normalized
        priority = int(contact.get("emergency_priority", 999))  # Default to low priority if not specified
        heapq.heappush(self.heap, (priority, contact["name"].lower(), contact["id"], copy.deepcopy(contact))) # Use a tuple to ensure proper ordering by priority, then name, then ID for tie-breaking

    def pop(self):
        if not self.heap:
            return None
        return heapq.heappop(self.heap)[3]  # Return the contact with the highest priority (lowest emergency_priority value)
    
    def is_empty(self):
        return len(self.heap) == 0
    
    def clear(self):
        self.heap = []

    def to_sorted_list(self):
        return [item[3] for item in sorted(self.heap)]

emergency_queue = EmergencyPriorityQueue()

def rebuild_emergency_queue():
    global emergency_queue
    emergency_queue = EmergencyPriorityQueue()  # Reset the emergency queue

    for contact in contacts:
        normalize_contact_structure(contact)  # Ensure contact structure is normalized before adding to emergency queue
        emergency_queue.push(contact)  # Add contact to emergency queue based on its emergency_priority

# -------------------------Homework 4 Requirement Emergency Priority Queue (HEAP) END-------------------------

# -------------------------Homework 4 Category Tree Global BEGIN-----

category_tree = CategoryTree()

def rebuild_category_tree():
    global category_tree
    category_tree = CategoryTree()  # Reset the category tree

    for contact in contacts:
        normalize_contact_structure(contact)
        category_tree.insert_contact(contact)

def rebuild_all_structures():
    ensure_ids()  # Ensure all contacts have IDs for consistency
    index_contacts()  # Rebuild hash index for O(1) search
    rebuild_category_bst()  # Rebuild category BST for organized display
    rebuild_category_tree()  # Rebuild category tree for organized display
    rebuild_emergency_queue()  # Rebuild emergency priority queue for emergency contact management

rebuild_all_structures()  # Initial build of all structures based on the initial contacts


# ---------------------------- ROUTES --------------------------------

# Add a sort route for session 9, which will sort the contacts alphabetically by name using Quick sort 
@app.route('/sort', methods=['POST'])
def sort_contacts():
    global contacts

    clear_redo_queue() # Session 7: Clear redo queue when a new action is performed after an undo, to maintain correct redo state
    
    contacts_list = [copy.deepcopy(c) for c in contacts]  # Convert linked list to a list for sorting

    if len(contacts_list) > 1:
        quick_sort(contacts_list, 0, len(contacts_list) - 1)  # Sort the list using Quick sort from session 10
   
    contacts = LinkedList()
    for contact in contacts_list:
        contacts.append(contact)

    rebuild_all_structures() # Rebuild all structures after sorting to ensure they reflect the new order, can be optimized if needed
    log_activity("Sorted contacts alphabetically (Quick Sort)") #Session 7 Activity Log

    return redirect(url_for('index'))

@app.route('/search')
def search_contact():
    query = request.args.get('query', '') # ****Double Check this is the correct way to get query parameter in Flask****
    result = find_contact_by_name(query)

    log_activity(f"Search: {query} -> {'Found' if result else 'Not Found'}")

    if result:
        return f"Contact found: {result['name']} ({result['email']})"
    else:
        return "Contact not found."
    

# ------------------------ Routes Session 13 Start "search ID" ----------------------------
@app.route('/search_id')
def search_contact_by_id():
    query = request.args.get('id', '').strip() # Get the 'id' query parameter and remove any leading/trailing whitespace
    
    if not query.isdigit():
        log_activity(f"Search by ID failed: Invalid ID '{query}'") #Session 7 Activity Log
        return "Invalid ID. Please enter a numeric ID."
    
    target_id = int(query)

    # Convert Linkedlist to list, then ensure sorted by id for binary search
    contacts_list = [c for c in contacts]  # Convert linked list to a list for searching
    contacts_list.sort(key=lambda c: c["id"])  # Ensure the list is sorted by ID for binary search

    result = binary_search_by_id(contacts_list, target_id)

    log_activity(f"Search by ID: {query} -> {'Found' if result else 'Not Found'}") #Session 7 Activity Log

    if result:
        return f"Contact found: {result['name']} ({result['email']}) with ID {result['id']}"
    
    return "Contact not found."

# ------------------------ Routes Session 13 End "search ID" ----------------------------

# ---------------------- Routes Search the BST by Full Category path BEGIN----------------------------

@app.route('/search_category')
def search_category():
    query = request.args.get('path', '').strip()

    if not query:
        return "Please provide a category path like: Work > Engineering > Platform"

    exists = category_bst.search(query)
    log_activity(f"Search category path: {query} -> {'Found' if exists else 'Not Found'}")

    if exists:
        return f"Category path found in BST: {query}"
    return f"Category path not found in BST: {query}"

# ----------------------- Routes Search the BST by Full Category path END----------------------------

@app.route('/')
def index():

    rebuild_all_structures() # Session 16: Rebuild category BST on each page load to ensure it reflects the current contacts, can be optimized if needed
    # Session 16: Build the category tree and pass it to the template for display
    tree_contacts_simple = build_tree_from_contacts(contacts)

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
                         activities=activity_queue.data, #Pass queue data to template
                         category_tree_contacts=category_tree.to_nested_dict(), # Session 16: Pass the category tree as a nested dictionary to the template for display
                         tree_contacts=tree_contacts_simple, # Session 16: Pass the tree-structured contacts to the template for display
                         bst_categories=category_bst.inorder(), # Session 16: Get sorted categories from the BST for display
                         emergency_contacts=emergency_queue.to_sorted_list() # Session 16: Get emergency contacts sorted by priority for display
                         )


@app.route('/add', methods=['POST'])
def add_contact():
    global next_id # Session 13: Access the global next_id variable to assign unique IDs to new contacts

    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()

    # Session 16: Get category and subcategory from the form, default to empty string if not provided
    category = request.form.get('category', '').strip()
    subcategory = request.form.get('subcategory', '').strip()

    # -----------------New BEGIN: add for homework 4 rquirements
    department = request.form.get('department', '').strip()
    team = request.form.get('team', '').strip()
    emergency_priority = request.form.get('emergency_priority', '').strip()

    if not name or not email:
        return redirect(url_for('index'))
    
    if emergency_priority == "":
        emergency_priority = 999  # Default low priority if not provided

    try:
        emergency_priority = int(emergency_priority)
    except ValueError:
        emergency_priority = 999  # Default low priority if conversion fails

    #-----------------New END: add for homework 4 requirements 


    clear_redo_queue() # Session 7: Clear redo queue when a new action is performed after an undo, to maintain correct redo state
    
    # 1. snapshot before add
    undo_add_stack.push(contacts.clone())

    if not department:
        if subcategory == "Engineers":
            department = "Engineering"
        elif subcategory == "HR":
            department = "HR"
        else:            
            department = "General"

    if not team:
        team = "General"

    # Session 16: Save category and subcategory with the contact
    new_contact = {
        "id": next_id,  # Assign a unique ID to the new contact
        "name": name,
        "email": email,
        "category": category,
        "subcategory": subcategory,
        "department": department,
        "team": team,
        "emergency_priority": emergency_priority
    }

    next_id += 1
    contacts.append(new_contact)

    added_contacts_stack.push(copy.deepcopy(new_contact))
    actions_stack.push("A")

    rebuild_all_structures()
    log_activity(
        f"Added contact: {name} ({email}) | "
        f"Path: {new_contact['category']} > {new_contact['department']} > {new_contact['team']} | "
        f"Emergency Priority: {emergency_priority}"
    )

    return redirect(url_for('index'))

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
        deleted_stack.push(copy.deepcopy(removed))
        actions_stack.push("D")

        index_contacts() # Rebuild hash index after modification
        rebuild_category_bst() # Session 16: Rebuild category BST after deletion, if we are using the BST for category organization

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
            rebuild_category_bst() # Session 16: Rebuild category BST after undoing an addition, if we are using the BST for category organization
            log_activity(f"Undo: Removed added contact: {last_added_contact['name']}") #Session 7 Activity Log

    elif last_action == "D":
        # Undo Delete: Restore the last deleted contact
        deleted = deleted_stack.pop()

        if deleted is not None  :
            contacts.append(copy.deepcopy(deleted))
            redo_queue.append(("D", copy.deepcopy(deleted)))  # Store deleted contact for redo
           
            index_contacts() # Rebuild hash index after modification
            rebuild_category_bst() # Session 16: Rebuild category BST after undoing a deletion, if we are using the BST for category organization
            log_activity(f"Undo: Restored deleted contact: {deleted['name']}") #Session 7 Activity Log
    return redirect(url_for('index'))

@app.route('/redo', methods=['POST'])
def redo_action():
    global contacts
    
    if not redo_queue:
        log_activity("Redo failed: No actions to redo") #Session 7 Activity Log
        return redirect(url_for('index'))

    action, contacts_snapshot = redo_queue.popleft() # *****Double check this line

    if contacts_snapshot is None:
        clear_redo_queue()  # Clear redo queue if snapshot is invalid
        log_activity("Redo failed: Invalid snapshot") #Session 7 Activity Log
        return redirect(url_for('index'))

    if action == "A":
        contacts.append(copy.deepcopy(contacts_snapshot))
        actions_stack.push("A")
       
        rebuild_all_structures() # Session 16: Rebuild all structures after redoing an addition, if we are using the BST for category organization
        log_activity(f"Redo: Re-added contact: {contacts_snapshot['name']}") #Session 7 Activity Log

    elif action == "D":
        removed = contacts.remove_by_name(contacts_snapshot["name"])
        if removed:
            deleted_stack.push(copy.deepcopy(removed))  # Push the removed contact to the deleted stack for potential future undos
            actions_stack.push("D")
            rebuild_all_structures() # Session 16: Rebuild all structures after redoing a deletion, if we are using the BST for category organization
            log_activity(f"Redo: Deleted contact again: {contacts_snapshot['name']}") #Session 7 Activity Log
        else:
            log_activity(f"Redo failed: Contact not found for deletion: {contacts_snapshot['name']}") #Session 7 Activity Log
    return redirect(url_for('index'))
                                                                                                    
# --- DATABASE CONNECTIVITY (For later phases) ---
# Placeholders for students to fill in during Sessions 5 and 27
def get_postgres_connection():
    pass

def get_mssql_connection():
    pass

if __name__ == '__main__':
    rebuild_all_structures() # Session 16: Build the category BST before starting the app, to ensure it's ready for use in the index route and other operations
    # Run the Flask app on port 5000, accessible externally
    app.run(host='0.0.0.0', port=5000, debug=True)
