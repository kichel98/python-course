# author: Piotr Andrzejewski
from collections import deque
import random


def generate_random_line(height, idx=1):
    if height < 1:
        return None
    subtree = generate_random_line(height - 1, idx + 1)
    if random.random() < 0.5:
        return [idx, subtree, None]
    else:
        return [idx, None, subtree]


def add_nodes_to_line(height, line, idx):
    if height < 1:
        return idx
    for i in range(1, len(line)):
        if line[i]:
            idx = add_nodes_to_line(height - 1, line[i], idx)
        elif random.random() < 0.5:
            line[i] = [idx + 1, None, None]
            idx = add_nodes_to_line(height - 1, line[i], idx + 1)
    return idx


def generate_random_tree(height):
    tree = generate_random_line(height)
    add_nodes_to_line(height - 1, tree, height)
    return tree


def dfs(tree):
    if not tree:
        return

    yield tree[0]
    for subtree in tree[1:]:
        yield from dfs(subtree)


def bfs(tree):
    if not tree:
        return

    q = deque()
    q.append(tree)
    while q:
        v = q.popleft()
        yield v[0]
        for subtree in v[1:]:
            if subtree:
                q.append(subtree)
    pass


rand_tree = generate_random_tree(4)
print(rand_tree)

print("DFS:")
gen = dfs(rand_tree)
for node in gen:
    print(node)

print("BFS:")
gen2 = bfs(rand_tree)
for node in gen2:
    print(node)



