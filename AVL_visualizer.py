import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx

class TreeNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def insert_bst(self, root, key):
        """Insert into BST without balancing."""
        if not root:
            return TreeNode(key)
        elif key < root.key:
            root.left = self.insert_bst(root.left, key)
        else:
            root.right = self.insert_bst(root.right, key)
        return root

    def insert_avl(self, root, key):
        """Insert into AVL Tree with balancing."""
        if not root:
            return TreeNode(key)
        elif key < root.key:
            root.left = self.insert_avl(root.left, key)
        else:
            root.right = self.insert_avl(root.right, key)

        # Update height of the current node
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        # Balance the node
        balance = self.get_balance(root)

        # Left Left Case
        if balance > 1 and key < root.left.key:
            return self.right_rotate(root)

        # Right Right Case
        if balance < -1 and key > root.right.key:
            return self.left_rotate(root)

        # Left Right Case
        if balance > 1 and key > root.left.key:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        # Right Left Case
        if balance < -1 and key < root.right.key:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def right_rotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def get_height(self, root):
        if not root:
            return 0
        return root.height

    def get_balance(self, root):
        if not root:
            return 0
        return self.get_height(root.left) - self.get_height(root.right)

def draw_tree(root, graph=None, pos=None, x=0, y=0, level_width=2, level_spacing=1):
    if graph is None:
        graph = nx.DiGraph()
    if pos is None:
        pos = {}
    if root:
        graph.add_node(root.key)
        pos[root.key] = (x, y)
        if root.left:
            graph.add_edge(root.key, root.left.key)
            draw_tree(root.left, graph, pos, x - level_width, y - level_spacing, level_width / 2, level_spacing)
        if root.right:
            graph.add_edge(root.key, root.right.key)
            draw_tree(root.right, graph, pos, x + level_width, y - level_spacing, level_width / 2, level_spacing)
    return graph, pos

def plot_tree(root, title="Binary Tree"):
    graph, pos = draw_tree(root)
    plt.figure(figsize=(10, 6))
    nx.draw(graph, pos, with_labels=True, node_size=2000, node_color="lightblue", font_size=10, font_weight="bold")
    plt.title(title)
    st.pyplot(plt)

# Streamlit App
st.title("BST to AVL Tree Visualization")

# Input for nodes
nodes_input = st.text_input("Enter comma-separated node values to create a tree:", "10,20,30,40,50,25")
nodes = list(map(int, nodes_input.split(",")))

# Unbalanced BST creation
bst = AVLTree()
unbalanced_root = None
for node in nodes:
    unbalanced_root = bst.insert_bst(unbalanced_root, node)

# Show unbalanced tree
st.header("Unbalanced Binary Search Tree")
if unbalanced_root:
    plot_tree(unbalanced_root, title="Unbalanced Binary Search Tree")

# Step-by-step AVL conversion
st.header("Step-by-Step AVL Tree Conversion")
avl_root = None
for i, node in enumerate(nodes):
    st.subheader(f"Step {i + 1}: Insert {node}")
    avl_root = bst.insert_avl(avl_root, node)
    plot_tree(avl_root, title=f"Tree after balancing {node}")
