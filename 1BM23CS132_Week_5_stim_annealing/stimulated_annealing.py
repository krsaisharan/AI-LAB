import random, math

def heuristic(state):
    n = len(state)
    attacks = 0
    for i in range(n):
        for j in range(i + 1, n):
            if abs(state[i] - state[j]) == abs(i - j):
                attacks += 1
    return attacks

def get_neighbor(state):
    n = len(state)
    i, j = random.sample(range(n), 2)
    neighbor = state[:]
    neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
    return neighbor

def simulated_annealing(state, T=100.0, cooling=0.9, max_steps=10000):
    cost = heuristic(state)
    print(f"Initial state: {state}, h = {cost}")
    for step in range(max_steps):
        if cost == 0:
            print(f"\nSolution found: {state} at step {step}")
            return state
        neighbor = get_neighbor(state)
        new_cost = heuristic(neighbor)
        delta = new_cost - cost
        if delta < 0 or random.random() < math.exp(-delta / T):
            state, cost = neighbor, new_cost
        print(f"Step {step+1}: {state}, h = {cost}, T = {T:.4f}")
        T *= cooling
    print("\nMax steps reached — Best found:", state, "with h =", cost)
    return state

initial = list(map(int, input("Enter initial 4-queen state (e.g. 2 3 0 1): ").split()))
simulated_annealing(initial)
