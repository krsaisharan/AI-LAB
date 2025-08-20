class SimpleReflexAgent:
    def __init__(self, location="A"):
        self.location = location

    def act(self, environment):
        if environment[self.location] == "Dirty":
            print(f"Vacuum in {self.location}: CLEAN")
            environment[self.location] = "Clean"
        else:
            self.location = "B" if self.location=="A" else "A"
            print(f"Vacuum moves to {self.location}")

class GoalBasedAgent:
    def __init__(self, location="A"):
        self.location = location

    def goal_reached(self, environment):
        return all(state=="Clean" for state in environment.values())

    def act(self, environment):
        if not self.goal_reached(environment):
            if environment[self.location] == "Dirty":
                print(f"Vacuum in {self.location}: CLEAN")
                environment[self.location] = "Clean"
            else:
                self.location = "B" if self.location=="A" else "A"
                print(f"Vacuum moves to {self.location}")
        else:
            print("✅ Goal Reached: All rooms clean")

# ---------- Simulation ----------
def simulate(agent, environment):
    print(f"\nInitial: {environment}, Vacuum at {agent.location}")
    steps=0
    while not isinstance(agent, GoalBasedAgent) or not agent.goal_reached(environment):
        agent.act(environment)
        steps+=1
        if steps>10: break
    print("Final:", environment, "\n")

# Example runs
env1 = {"A":"Dirty","B":"Dirty"}
print("=== Simple Reflex ===")
simulate(SimpleReflexAgent("A"), env1.copy())

env2 = {"A":"Clean","B":"Dirty"}
print("=== Goal Based ===")
simulate(GoalBasedAgent("A"), env2.copy())

