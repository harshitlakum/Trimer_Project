import subprocess
from itertools import product

shifts = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
runs = [1, 2, 3, 4]
base_seed = 123456  # you can change this if you want

processes = []
for shift, run in product(shifts, runs):
    cmd = [
        'python', 'trimer_sim.py',  
        '--shift', str(shift),
        '--run', str(run),
        '--base-seed', str(base_seed)
    ]
    print("Launching:", " ".join(cmd))
    # Use Popen to launch without waiting (parallel)
    p = subprocess.Popen(cmd)
    processes.append(p)

# Optionally: wait for all processes to finish
for p in processes:
    p.wait()

print("All jobs launched!")
