import random
import math
import matplotlib.pyplot as plt
import os


#read data
def parse_species(text):

    if not text or not text.strip():
        return {}
    parts = text.strip().split()
    res = {}
    for i in range(0, len(parts), 2):
        if i + 1 < len(parts):
            species = parts[i]
            try:
                count = int(parts[i+1])
                res[species] = res.get(species, 0) + count
            except ValueError:
                pass
    return res

def load_reactions(filename='lambda.r'):
    reactions = []
    all_species = set()
    
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        return [], set()

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): 
                continue
            
            parts = line.split(':')
            if len(parts) < 3:
                continue

            reactants = parse_species(parts[0])
            products = parse_species(parts[1])
            try:
                rate = float(parts[2])
            except ValueError:
                continue

            reactions.append({
                'reactants': reactants,
                'products': products,
                'k': rate
            })
            
            all_species.update(reactants.keys())
            all_species.update(products.keys())
            
    print(f"Loaded {len(reactions)} reactions from {filename}")
    return reactions, all_species

def load_initial_conditions(filename='lambda.in'):

    initial_counts = {}
    
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        return {}

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): 
                continue
            
            parts = line.split()
            if len(parts) >= 2:
                species = parts[0]
                try:
                    count = int(parts[1])
                    initial_counts[species] = count
                except ValueError:
                    continue
                    
    print(f"Loaded initial conditions for {len(initial_counts)} species from {filename}")
    return initial_counts

# Gillespie SSA implementation
def gillespie_ssa(start_state, reactions, max_steps=200000):
    state = start_state.copy()
    t = 0.0
    
    THRESHOLD_CI2 = 145
    THRESHOLD_CRO2 = 55
    
    for step in range(max_steps):
        if state.get('cI2', 0) > THRESHOLD_CI2:
            return "Stealth"
        if state.get('Cro2', 0) > THRESHOLD_CRO2:
            return "Hijack"
            
        # calculate propensities
        propensities = []
        total_propensity = 0.0
        
        for rxn in reactions:
            h = 1.0
            possible = True
            
            for sp, stoich in rxn['reactants'].items():
                n = state.get(sp, 0)
                if n < stoich:
                    possible = False
                    break
                
                if stoich == 1:
                    h *= n
                elif stoich == 2:
                    h *= n * (n - 1) * 0.5
                elif stoich == 3:
                    h *= n * (n - 1) * (n - 2) / 6.0
                else:
                    h *= math.comb(n, stoich)
            
            if possible:
                a = h * rxn['k']
            else:
                a = 0.0
                
            propensities.append(a)
            total_propensity += a
            
            
        r1 = random.random()
        if total_propensity > 0:
             tau = (1.0 / total_propensity) * math.log(1.0 / r1)
        else:
             tau = 0
        t += tau
        
        # determine which reaction occurs
        r2 = random.random()
        threshold_val = r2 * total_propensity
        running_sum = 0.0
        selected_rxn_idx = -1
        
        for i, p in enumerate(propensities):
            running_sum += p
            if running_sum >= threshold_val:
                selected_rxn_idx = i
                break
        
        if selected_rxn_idx != -1:
            rxn = reactions[selected_rxn_idx]
            
            for sp, stoich in rxn['reactants'].items():
                state[sp] = state.get(sp, 0) - stoich
                
            for sp, stoich in rxn['products'].items():
                state[sp] = state.get(sp, 0) + stoich
            
    return "Timeout"


def main():
    # Loaddata
    reactions, all_species = load_reactions('lambda.r')
    base_initials = load_initial_conditions('lambda.in')
    
    if not reactions or not base_initials:
        print("Failed to load necessary files. Exiting.")
        return

    for sp in all_species:
        if sp not in base_initials:
            base_initials[sp] = 0

    # set parameters for MOI simulation
    moi_values = range(1, 11)  # MOI from 1 to 10
    simulations_per_moi = 100  #runs per MOI for 100 times
    
    prob_stealth = []
    prob_hijack = []

    print(f"\nStarting Simulations ({simulations_per_moi} runs per MOI)...")
    print("-" * 50)
    print(f"{'MOI':<5} | {'P(Stealth)':<12} | {'P(Hijack)':<12} | {'Valid Runs'}")
    print("-" * 50)

    #change moi and run simulations
    for moi in moi_values:
        stealth_count = 0
        hijack_count = 0
        
        current_state = base_initials.copy()
        
        current_state['MOI'] = moi
        
        genomic_sites = ['OR', 'PRE', 'NUTR4', 'NUTL', 'OL', 'NUTR', 'NUTR3', 'NUTR2', 'P1', 'P2']
        for site in genomic_sites:
            if site in current_state and current_state[site] <= 1:
                 current_state[site] = moi
            elif site not in current_state:
                 current_state[site] = moi

        for _ in range(simulations_per_moi):
            result = gillespie_ssa(current_state, reactions)
            if result == "Stealth":
                stealth_count += 1
            elif result == "Hijack":
                hijack_count += 1
        
        #calculate probabilities
        valid_runs = stealth_count + hijack_count
        if valid_runs > 0:
            p_s = stealth_count / valid_runs
            p_h = hijack_count / valid_runs
        else:
            p_s = 0.0
            p_h = 0.0
            
        prob_stealth.append(p_s)
        prob_hijack.append(p_h)
        
        print(f"{moi:<5} | {p_s:<12.2f} | {p_h:<12.2f} | {valid_runs}/{simulations_per_moi}")

    #draw plot
    plt.figure(figsize=(10, 6))
    plt.plot(moi_values, prob_stealth, 'b-o', label='Lysogeny (Stealth)', linewidth=2)
    plt.plot(moi_values, prob_hijack, 'r-x', label='Lysis (Hijack)', linewidth=2)
    
    plt.title('Lambda Phage Fate Decision vs. MOI')
    plt.xlabel('Multiplicity of Infection (MOI)')
    plt.ylabel('Probability')
    plt.xticks(moi_values)
    plt.ylim(-0.05, 1.05)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    
    plt.savefig('lambda_simulation_results.png')
    print("\nSimulation complete. Plot saved as 'lambda_simulation_results.png'.")
    plt.show()

if __name__ == "__main__":
    main()
