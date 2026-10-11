# Quick start: a calculation without nuclear libraries

**Goal:** verify matrix assembly, solver dispatch, export, and time averaging before configuring the GUI databases.

From the repository root after [installation](installation.md):

```powershell
.\.venv\Scripts\python.exe examples/documentation_quickstart.py
```

On Linux/macOS use `.venv/bin/python` instead. You can choose an output directory with `--output`.

## Model and expected result

The script constructs a synthetic two-species chain with transition rate 1 per second and a stable daughter. Labels Fe-56 and Co-56 exercise the isotope API; the assigned rate and stability are deliberately artificial and are not evaluated properties of these nuclides. Initial inventories are `[1, 0]`, with zero neutron flux and no neutron reactions.

At time $t$ in seconds, the analytical inventories are

$$N_1(t)=e^{-t},\qquad N_2(t)=1-e^{-t}.$$

At 2 s, they are approximately **0.1353352832** and **0.8646647168**. Their sum remains one. The script checks Padé, ordinary CRAM-16, adaptive CRAM-16, and IPF CRAM-48 against this solution.

A uniform average over 0–2 s gives approximately **0.4323323584** and **0.5676676416**. The trapezoidal approximation on 2001 points is checked against these values. This exercises the same averaging backend used by the GUI.

## Output

- `results/documentation_quickstart/evolution.csv`: each solver's saved inventories.
- `results/documentation_quickstart/verification.json`: maximum errors, mean inventories, Python version, and pass status.

The script exits with an error if its checks fail. Passing this example verifies a small synthetic calculation, not a nuclear library or an astrophysical model.

```{literalinclude} ../examples/documentation_quickstart.py
:language: python
:caption: Complete reproducible example
```

Next, [connect your nuclear data](nuclear-data.md) and follow the [GUI workflow](user-guide.md).
