import numpy as np
import random

def calculate_propensities(state):
    x1, x2, x3 = state
    a1 = 0.5 * x1 * (x1 - 1) * x2 
    a2 = x1 * x3 * (x3 - 1) 
    a3 = 3 * x2 * x3 
    return [a1, a2, a3]

def run_simulation_outcome(initial_state, max_steps=10000):
    state = list(initial_state)
    
    updates = [[-2, -1, 4], [-1, 3, -2], [2, -1, -1]]
    
    for step in range(max_steps):
        x1, x2, x3 = state
        if x1 >= 150: return 1
        if x2 < 10:   return 2
        if x3 > 100:  return 3
        
        props = calculate_propensities(state)
        a_sum = sum(props)
        
        if a_sum == 0: return 0
        
        r = random.uniform(0, a_sum)
        cumulative = 0
        reaction_idx = -1
        for i, p in enumerate(props):
            cumulative += p
            if r <= cumulative:
                reaction_idx = i
                break
        
        update = updates[reaction_idx]
        for i in range(3):
            state[i] += update[i]
            
    return 0

def problem_1a():
    start_state = [110, 26, 55]
    counts = {1:0, 2:0, 3:0, 0:0}
    num_sims = 10000
    
    print(f"Running Problem 1(a) with {num_sims} simulations...")
    for i in range(num_sims):
        res = run_simulation_outcome(start_state)
        counts[res] += 1
        # print(i, end="\r")
        
    print("Problem 1(a) Results:")
    print(f"Pr(C1): {counts[1]/num_sims}")
    print(f"Pr(C2): {counts[2]/num_sims}")
    print(f"Pr(C3): {counts[3]/num_sims}")

def problem_1b():
    start_state = [9, 8, 7]
    final_x1, final_x2, final_x3 = [], [], []
    num_sims = 10000
    target_steps = 7
    
    updates = [[-2, -1, 4], [-1, 3, -2], [2, -1, -1]]

    for _ in range(num_sims):
        state = list(start_state)
        valid_run = True
        for _ in range(target_steps):
            props = calculate_propensities(state)
            a_sum = sum(props)
            if a_sum == 0: 
                valid_run = False; break
            
            r = random.uniform(0, a_sum)
            cumulative = 0
            reaction_idx = -1
            for i, p in enumerate(props):
                cumulative += p
                if r <= cumulative:
                    reaction_idx = i
                    break
            
            for i in range(3):
                state[i] += updates[reaction_idx][i]
        
        if valid_run:
            final_x1.append(state[0])
            final_x2.append(state[1])
            final_x3.append(state[2])

    print("\nProblem 1(b) Results:")
    print(f"X1: Mean={np.mean(final_x1):.4f}, Var={np.var(final_x1):.4f}")
    print(f"X2: Mean={np.mean(final_x2):.4f}, Var={np.var(final_x2):.4f}")
    print(f"X3: Mean={np.mean(final_x3):.4f}, Var={np.var(final_x3):.4f}")

if __name__ == "__main__":
    print("Running Problem 1(a)...")
    problem_1a()
    print("Running Problem 1(b)...")
    problem_1b()