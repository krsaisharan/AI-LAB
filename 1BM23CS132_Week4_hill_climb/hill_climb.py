import random

def calculate_cost(state):
    cost = 0
    n = len(state)
    for i in range(n):
        for j in range(i+1, n):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                cost += 1
    return cost

def generate_neighbors(state):
    neighbors = []
    n = len(state)
    for col in range(n):
        for row in range(n):
            if row != state[col]:
                neighbor = state[:]
                neighbor[col] = row
                neighbors.append(neighbor)
    return neighbors

def hill_climbing(state):
    current = state[:]
    current_cost = calculate_cost(current)
    print(f"Initial state: {current}, cost = {current_cost}")
    while True:
        neighbors = generate_neighbors(current)
        neighbor_costs = [(calculate_cost(neigh), neigh) for neigh in neighbors]
        best_cost, best_neighbor = min(neighbor_costs, key=lambda x: x[0])
        print(f"Best neighbor: {best_neighbor}, cost = {best_cost}")
        if best_cost < current_cost:
            current, current_cost = best_neighbor, best_cost
        else:
            break
    return current, current_cost

if __name__ == "__main__":
    initial = list(map(int, input("Enter initial 4-queen state (e.g. 2 3 0 1): ").split()))
    solution, cost = hill_climbing(initial)
    if cost == 0:
        print("Solution found:", solution)
    else:
        print("Local optimum reached:", solution, "cost =", cost)
