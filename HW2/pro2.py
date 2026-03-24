import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

def biquad_sim_5_runs():
    kf = 100.0  
    period_duration = 100 
    
    input_sequence = [100, 5, 500, 20, 250]
    theory_values = [12.50, 14.69, 79.02, 77.34, 115.80] 
    
    mem = {'xp1': 0.0, 'xp2': 0.0, 'yp1': 0.0, 'yp2': 0.0}

    def odes(t, y, x_now, xp1, xp2, yp1, yp2):
        target_Y = 0.125 * (x_now + xp1 + xp2 + yp1 + yp2)
        dYdt = kf * (target_Y - y[0])
        return [dYdt]

    all_t, all_y = [], []
    current_Y_state = [0.0]
    start_time = 0

    print(f"{'Run Time':<6} | {'Input X':<8} | {'Output Y':<10} | {'Theoretical Value'}")
    print("-" * 50)

    for i, x_val in enumerate(input_sequence):
        sol = solve_ivp(odes, (start_time, start_time + period_duration), current_Y_state, 
                        args=(x_val, mem['xp1'], mem['xp2'], mem['yp1'], mem['yp2']),
                        method='Radau', t_eval=np.linspace(start_time, start_time + period_duration, 500))
        
        all_t.extend(sol.t)
        all_y.extend(sol.y[0])
        
        final_Y = sol.y[0, -1]
        print(f"n={i+1:<4} | {x_val:<8} | {final_Y:<10.2f} | {theory_values[i]:.2f}")
        
        mem['yp2'], mem['yp1'] = mem['yp1'], final_Y
        mem['xp2'], mem['xp1'] = mem['xp1'], x_val
        current_Y_state = [final_Y]
        start_time += period_duration

    all_y = np.array(all_y)
    t_plot = np.array(all_t)
    
    plt.figure(figsize=(12, 8))
    plt.subplot(2, 1, 1)
    plt.plot(t_plot, all_y, 'r-', lw=2, label='Output Y (Simulated)')
    plt.title(f'Biquad CRN Simulation (5 Runs, Total Time: {start_time}s)')
    plt.ylabel('Concentration'); plt.legend(); plt.grid(True, alpha=0.3)
    plt.subplot(2, 1, 2)
    t_mod = t_plot % period_duration

    plt.plot(t_plot, np.where(t_mod < 33, 1.0, 0.0), 'r--', label='Ind: r')
    plt.plot(t_plot, np.where((t_mod >= 33) & (t_mod < 66), 1.0, 0.0), 'g--', label='Ind: g')
    plt.plot(t_plot, np.where(t_mod >= 66, 1.0, 0.0), 'b--', label='Ind: b')
    plt.title('Corrected RGB Indicators (Phase Control)')
    plt.xlabel('Time (s)'); plt.ylabel('Activity'); plt.legend(); plt.grid(True, alpha=0.3)

    plt.tight_layout(); plt.show()

if __name__ == "__main__":
    biquad_sim_5_runs()