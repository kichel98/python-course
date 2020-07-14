# author: Piotr Andrzejewski
from collections import deque
import random


class Node(object):
    def __init__(self, val, children=None):
        if children is None:
            children = []
        self.val = val
        self.children = children

    def __str__(self):
        children_str = ", ".join([str(child) for child in self.children])
        return f"({self.val}, [{children_str}])"

    def add_child(self, child):
        self.children.append(child)

    def get_child(self, idx=0):
        return self.children[idx]


def generate_line(height):
    if height < 1:
        return None
    root = Node(1)
    node = root
    for idx in range(height - 1):
        child = Node(idx + 2)
        node.add_child(child)
        node = child
    return root


def add_nodes_to_line(height, node, idx):
    if height < 1:
        return idx

    if random.random() < 0.5:
        min_child, max_child = 1, 5
        children_count = random.randint(min_child, max_child)
        new_children = []
        for i in range(children_count):
            new_child = Node(idx+1)
            idx = add_nodes_to_line(height - 1, new_child, idx + 1)
            new_children.append(new_child)
        if node.children:
            child_new_idx = random.randint(0, children_count - 1)
            new_children[child_new_idx] = node.get_child()
        node.children = new_children
    elif node.children:
        idx = add_nodes_to_line(height - 1, node.get_child(), idx)
    return idx


def generate_random_tree(height):
    tree = generate_line(height)
    add_nodes_to_line(height - 1, tree, height)
    return tree


def dfs(node):
    if not node:
        return

    yield node.val
    if node.children:
        for child in node.children:
            yield from dfs(child)


def bfs(node):
    if not node:
        return

    q = deque()
    q.append(node)
    while q:
        v = q.popleft()
        yield v.val
        if v.children:
            for child in v.children:
                q.append(child)
    pass


rand_tree = generate_random_tree(4)
print(rand_tree)

print("DFS")
gen = dfs(rand_tree)
for node in gen:
    print(node)

print("BFS")
gen2 = bfs(rand_tree)
for node in gen2:
    print(node)

