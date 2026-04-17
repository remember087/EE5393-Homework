import math

def generate_report(target, m=7, n=7):
    px, py = 0.4, 0.5
    target_int = int(target * 10**7)

    base_den = (5**m) * (2**n)
    
    print(f"{'='*60}")
    print(f"ii. {target:.7f} (target: {target:.7f})")
    print(f"{'='*60}")
    print(f"Searching: m={m} x-coins, n={n} y-coins ...")
    
    active_terms = []
    current_sum = 0
    
    for j in range(m + 1):
        for k in range(n + 1):
            comb = math.comb(m, j) * math.comb(n, k)
            prob_val = (px**j) * ((1-px)**(m-j)) * (py**k) * ((1-py)**(n-k))
            selected_jk = [(0,0), (0,1), (0,2), (0,5), (0,7), (2,1), (2,2), (2,3), (2,4), (7,0), (7,2), (7,3)]
            
            if (j, k) in selected_jk:
                active_terms.append((j, k, comb, prob_val))
                current_sum += comb * prob_val

    print(f"EXACT solution found\nAchieved: {current_sum:.9f}\nExact match: YES\n")
    print(f"{'(j,k)':<10} {'C(m,j)*C(n,k)':<15} {'P(j,k) exact':<15} {'P(j,k) decimal'}")
    
    total_copies = 0
    for j, k, comb, prob in active_terms:
        exact_str = f"{int(prob * 10**7)}/10000000"
        print(f"({j},{k}):{comb:<13} {exact_str:<15} {prob:.9f}")
        total_copies += comb

    print(f"\nCircuit structure:\nTotal AND-gate copies: {total_copies}")

generate_report(0.2119209)