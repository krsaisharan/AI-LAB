from collections import deque

def print_board(state):
    for i in range(0, 9, 3):
        print(state[i:i+3])
    print()

def get_neighbors(state):
    neighbors = []
    idx = state.index('0')
    row, col = divmod(idx, 3)
    moves = [(-1,0),(1,0),(0,-1),(0,1)]
    for dr, dc in moves:
        r, c = row + dr, col + dc
        if 0 <= r < 3 and 0 <= c < 3:
            new_idx = r*3 + c
            state_list = list(state)
            state_list[idx], state_list[new_idx] = state_list[new_idx], state_list[idx]
            neighbors.append("".join(state_list))
    return neighbors

def dfs(start, goal, limit=50):
    stack = [(start, [start])]
    visited = set()
    while stack:
        state, path = stack.pop()
        if state == goal:
            return path
        if state not in visited and len(path) <= limit:
            visited.add(state)
            for neighbor in get_neighbors(state):
                stack.append((neighbor, path + [neighbor]))
    return None

def dls(state, goal, depth, path, visited):
    if state == goal:
        return path
    if depth == 0:
        return None
    visited.add(state)
    for neighbor in get_neighbors(state):
        if neighbor not in visited:
            res = dls(neighbor, goal, depth-1, path+[neighbor], visited)
            if res:
                return res
    visited.remove(state)
    return None

def iddfs(start, goal, max_depth=20):
    for depth in range(max_depth+1):
        visited = set()
        result = dls(start, goal, depth, [start], visited)
        if result:
            return result
    return None

if __name__ == "__main__":
    start = "283164705"
    goal  = "123804765"

    print("DFS Solution:")
    path_dfs = dfs(start, goal, limit=50)
    if path_dfs:
        for state in path_dfs:
            print_board(state)
    else:
        print("No solution found with DFS")

    print("IDS Solution:")
    path_ids = iddfs(start, goal, max_depth=20)
    if path_ids:
        for state in path_ids:
            print_board(state)
    else:
        print("No solution found with IDS")

