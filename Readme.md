# Field-Controlled Assembly of Shifted-Dipole Trimers

This repository accompanies the project:

**Field-Controlled Assembly and Structural Transitions in Shifted-Dipole Trimer Clusters: ESPResSo Simulations and Order-Parameter Analysis**  
*Harshit Lakum, Department of Physics, Universität Wien (July 2025)*

---

## 📖 Contents
- `Analyze_Trimer.py` → Post-processing script to compute the order parameter **S** from VTF trajectories and generate histograms.
- `run_all.py` → Batch launcher to run multiple simulations across different shifts and runs (requires private simulation script).
- `paper.pdf` → Full project paper draft with methods, results, and discussion.
- `results/` → Example histograms of P(S) for different shifts.
- `videos/` → Example `.mpg` videos of trimer cluster dynamics.

⚠️ **Note on simulation code**  
The main simulation engine `trimer_sim.py` is **kept private** and is excluded from this repository. If you are interested in collaboration or access, please contact me directly.

---

## 🚀 Usage

### 1. Running Simulations
Simulations require the private `trimer_sim.py` file, which is not included here. Once available, you can launch simulations via:
```bash
python run_all.py
````

### 2. Analyzing Results

After simulations generate `.vtf` trajectory files, compute the order parameter histograms:

```bash
python Analyze_Trimer.py --data-dir results \
    --shifts 0.0 0.1 0.2 0.3 0.4 0.5 \
    --runs 1 2 3 4 \
    --segment-lengths 500 100 2000 100 2000
```

Histograms will be saved into the `results/` folder.

---

## 📊 Example Results

* **Linear chains (a ≤ 0.3):** Histograms peak at S ≈ 1.
* **Disordered/bent regime (0.4 ≲ a ≲ 0.55):** Broad P(S) distributions.
* **Triangular states (a ≥ 0.6):** Sharp peaks near S ≈ 0.59.

See `results/` for generated plots.

---

## 🎥 Videos

The `videos/` folder contains representative `.mpg` files of trimer dynamics under different dipole shifts:

* `0.1.mpg`
* `0.5.mpg`
* `0.8.mpg`

---

## 📚 References

1. Kantorovich et al., *Soft Matter* **7**, 5217–5227 (2011).
2. Steinbach et al., *Soft Matter* **12**, 2737–2743 (2016).
3. Steinbach et al., *Phys. Rev. E* **100**, 012608 (2019).
4. Steinbach et al., *Phys. Rev. Research* **2**, 023092 (2020).
5. [ESPResSo Documentation](https://espressomd.github.io/doc4.2.2/index.html)

---

## 📝 License

This repository is released under the MIT License, except for `trimer_sim.py`, which is private and not distributed.




