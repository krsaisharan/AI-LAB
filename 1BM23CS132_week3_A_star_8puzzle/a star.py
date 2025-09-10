import heapq

class Node:
    def __init__(self, state, parent=None, g=0):
        self.state = state
        self.parent = parent
        self.g = g
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        return self.f < other.f

def misplaced_tiles(state, goal):
    return sum(1 for i in range(9) if state[i] != 0 and state[i] != goal[i])

def manhattan_distance(state, goal):
    distance = 0
    for i in range(1, 9):
        xi, yi = divmod(state.index(i), 3)
        xg, yg = divmod(goal.index(i), 3)
        distance += abs(xi - xg) + abs(yi - yg)
    return distance

def get_neighbors(node):
    neighbors = []
    s = node.state
    idx = s.index(0)
    x, y = divmod(idx, 3)
    moves = [(-1,0),(1,0),(0,-1),(0,1)]
    for dx, dy in moves:
        nx, ny = x+dx, y+dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = s.copy()
            new_idx = nx*3 + ny
            new_state[idx], new_state[new_idx] = new_state[new_idx], new_state[idx]
            neighbors.append(Node(new_state, node, node.g+1))
    return neighbors

def reconstruct_path(node):
    path = []
    while node:
        path.append(node.state)
        node = node.parent
    return path[::-1]

def a_star(initial, goal, heuristic):
    open_list = []
    closed = set()

    root = Node(initial, None, 0)
    root.h = heuristic(root.state, goal)
    root.f = root.g + root.h
    heapq.heappush(open_list, root)

    while open_list:
        current = heapq.heappop(open_list)

        if current.state == goal:
            return reconstruct_path(current)

        closed.add(tuple(current.state))

        for neighbor in get_neighbors(current):
            if tuple(neighbor.state) in closed:
                continue
            neighbor.h = heuristic(neighbor.state, goal)
            neighbor.f = neighbor.g + neighbor.h
            heapq.heappush(open_list, neighbor)

    return None

if __name__ == "__main__":
    initial = [0,1,3,
               4,2,5,
               7,8,6]

    goal = [1,2,3,
            4,5,6,
            7,8,0]

    print("Using Misplaced Tiles Heuristic:")
    path1 = a_star(initial, goal, misplaced_tiles)
    for depth, state in enumerate(path1):
        print(f"Depth {depth}:")
        for i in range(0,9,3):
            print(state[i:i+3])
        print()

    print("Using Manhattan Distance Heuristic:")
    path2 = a_star(initial, goal, manhattan_distance)
    for depth, state in enumerate(path2):
        print(f"Depth {depth}:")
        for i in range(0,9,3):
            print(state[i:i+3])
        print()
