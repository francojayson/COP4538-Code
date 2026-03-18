class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

# Create all the nodes
root = TreeNode("All Contacts")
work = TreeNode("Work")
personal = TreeNode("Personal")
engineers = TreeNode("Engineers")
hr = TreeNode("HR")

# ...after node creation...

# Link the children to their parents
root.add_child(work)
root.add_child(personal)

work.add_child(engineers)
work.add_child(hr)

# Print the values of the root's direct children
for child in root.children:
    print(child.data)





