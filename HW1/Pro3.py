import numpy as np
import matplotlib.pyplot as plt

def run_simulation():
    print("Running Problem 3.1 Simulation...")
    
    Y0_input = 64  # Input Y
    X0_val = 5     # Multiplier X0
    t_end_31 = 10
    
    # State: [Y, Z]
    state_31 = [Y0_input, 0]
    
    t = 0
    t_hist_31 = [0]
    Y_hist_31 = [state_31[0]]
    Z_hist = [state_31[1]]
    
    while t < t_end_31 and state_31[0] >= 2:
        Y, Z = state_31
        
        a1 = 1.0 * Y if Y >= 2 else 0
        if a1 == 0:
            break
            
        tau = -np.log(np.random.rand()) / a1
        t += tau
        
        state_31[0] = Y // 2
        state_31[1] = Z + X0_val
        
        t_hist_31.append(t)
        Y_hist_31.append(state_31[0])
        Z_hist.append(state_31[1])

    theoretical_Z = X0_val * np.log2(Y0_input)


    print("Running Problem 3.2 Simulation...")
    
    X0_32 = 32      # Input X
    Y0_seed = 1     # Seed for exponential growth (starts at 1)
    t_end_32 = 10
    
    state_32 = [X0_32, 0, Y0_seed]
    
    t = 0
    t_hist_32 = [0]
    X_hist = [state_32[0]]
    L_hist = [state_32[1]]
    Y_hist_32 = [state_32[2]]
    
    while t < t_end_32 and (state_32[0] > 1 or state_32[1] > 0):
        X, L, Y = state_32
        
        a1 = 1.0 * X if X >= 2 else 0
        a2 = 50.0 if (L > 0 and Y > 0) else 0
        
        a0 = a1 + a2
        if a0 == 0:
            break
            
        # Gillespie time step
        tau = -np.log(np.random.rand()) / a0
        t += tau
        
        # Determine which reaction fires based on probability
        if np.random.rand() < a1 / a0:
            state_32[0] = X // 2
            state_32[1] = L + 1
        else:
            state_32[1] = L - 1
            state_32[2] = Y * 2
            
        # Record state
        t_hist_32.append(t)
        X_hist.append(state_32[0])
        L_hist.append(state_32[1])
        Y_hist_32.append(state_32[2])


#draw the plots
    plt.style.use('dark_background') 
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    # Plot 3.1
    ax1.step(t_hist_31, Y_hist_31, label='Y (Input)', where='post', linewidth=2, color='#4A90E2')
    ax1.step(t_hist_31, Z_hist, label='Z (Output)', where='post', linewidth=2, color='#E67E22')
    ax1.axhline(theoretical_Z, color='#E74C3C', linestyle='--', label='Theoretical Target')
    ax1.set_title(f'Prob 3.1: $Z = X_0 \log_2(Y_0)$. Inputs: $Y_0$={Y0_input}, $X_0$={X0_val}', fontweight='bold')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Count')
    ax1.grid(True, alpha=0.3)
    ax1.legend()

    # Plot 3.2
    ax2.step(t_hist_32, X_hist, label='X (Input)', where='post', linewidth=2, color='#4A90E2')
    ax2.step(t_hist_32, L_hist, label='L (Log Count)', where='post', linewidth=2, color='#F39C12')
    ax2.step(t_hist_32, Y_hist_32, label='Y (Output)', where='post', linewidth=2, color='#F1C40F')
    ax2.set_title(f'Prob 3.2: $Y = 2^{{\log_2(X_0)}}$. Input $X_0$={X0_32}, Final Y={Y_hist_32[-1]}', fontweight='bold')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Count')
    ax2.grid(True, alpha=0.3)
    ax2.legend()

    plt.tight_layout()
    plt.show()

    print("\n--- Simulation Results ---")
    print(f"Problem 3.1 Final Z: {Z_hist[-1]} (Theoretical Target: {theoretical_Z})")
    print(f"Problem 3.2 Final Y: {Y_hist_32[-1]} (Expected Target: {X0_32})")

if __name__ == "__main__":
    run_simulation()