def alphabeta(node, depth, alpha, beta, maximizingPlayer, tree, path, pruned):
    if isinstance(tree[node], (int, float)):
        return tree[node]

    if maximizingPlayer:
        maxEval = float('-inf')
        for child in tree[node]:
            val = alphabeta(child, depth + 1, alpha, beta, False, tree, path, pruned)
            maxEval = max(maxEval, val)
            alpha = max(alpha, val)
            if alpha >= beta:
                pruned.append((node, child))
                break
        path[node] = maxEval
        return maxEval
    else:
        minEval = float('inf')
        for child in tree[node]:
            val = alphabeta(child, depth + 1, alpha, beta, True, tree, path, pruned)
            minEval = min(minEval, val)
            beta = min(beta, val)
            if beta <= alpha:
                pruned.append((node, child))
                break
        path[node] = minEval
        return minEval


print("\n--- Alpha-Beta Pruning ---\n")
tree = {}

n = int(input("Enter number of internal (non-leaf) nodes: "))
for _ in range(n):
    parent = input("\nEnter parent node name: ").strip()
    children = input("Enter its children (space separated): ").strip().split()
    tree[parent] = children

print("\nEnter leaf node values (e.g. A=3 B=5 C=2):")
leaf_input = input("Values: ").strip().split()
for pair in leaf_input:
    k, v = pair.split("=")
    tree[k] = int(v)

root = input("\nEnter root node: ").strip()

path = {}
pruned = []

value = alphabeta(root, 0, float('-inf'), float('inf'), True, tree, path, pruned)

print("\n✅ Final Value at Root Node:", value)
print("\n📈 Path Values:", path)
print("\n✂️ Pruned Branches:", pruned)
