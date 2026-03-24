def fibonacci_molecular_sim(start_x, start_y, steps=12):
    X, Y = start_x, start_y
    history = [(X, Y)]
    
    print(f"Initial Concentration: X={X}, Y={Y}")
    
    for i in range(1, steps + 1):
        new_X = Y
        new_Y = X + Y
        X, Y = new_X, new_Y
        history.append((X, Y))
        print(f"Step {i:2d}  (S{i}): X={X}, Y={Y}")
    
    return Y

print("Case A: Initial Value 0, 1")
final_a = fibonacci_molecular_sim(0, 1, 12) 
print("\nCase B: Initial Value 3, 7")
final_b = fibonacci_molecular_sim(3, 7, 12)