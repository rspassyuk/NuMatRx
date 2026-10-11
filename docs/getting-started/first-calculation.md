# Your first calculation

This example runs in a few seconds and needs no nuclear libraries. It builds the simplest possible network — one unstable nuclide decaying into a stable one — solves it with every solver in NuMatRx, and compares the result with the exact answer.

## Run it

```bash
python examples/documentation_quickstart.py
```

Use the Python from your virtual environment (see {doc}`installation`). Add `--output my_folder` to choose where the results go.

## What it computes

Two nuclides with a decay rate $\lambda = 1\ \mathrm{s^{-1}}$ from the first to the second, starting from $N_1 = 1$, $N_2 = 0$. The exact solution is

$$
N_1(t) = e^{-t}, \qquad N_2(t) = 1 - e^{-t}.
$$

```{note}
The script labels the two nuclides Fe-56 and Co-56 only to exercise the isotope API. The decay rate is artificial — real Fe-56 is stable.
```

The script checks four solvers at $t = 0,\ 0.5,\ 1,\ 2,\ 5$ s:

| Solver | Name in code |
|---|---|
| Padé (SciPy) | `pade` |
| CRAM-16 | `cram16` |
| Adaptive CRAM-16 | `cram16_adaptive` |
| CRAM-48 | `cram48` |

It then averages the trajectory over $0 \le t \le 2$ s and compares with the exact mean values

$$
\langle N_1 \rangle = \frac{1 - e^{-2}}{2} \approx 0.4323, \qquad
\langle N_2 \rangle \approx 0.5677 .
$$

## What you get

```text
results/documentation_quickstart/
├── evolution.csv         inventories for every solver and time
└── verification.json     errors, mean values, "passed": true
```

At $t = 2$ s you should see $N_1 \approx 0.1353$ and $N_2 \approx 0.8647$, with errors below $10^{-9}$ for every solver.

## The code

The whole calculation takes a dozen lines. This is the core of it:

```python
from core.entities import Isotope, DecayLink
from core.burnup import BurnupConfig, BurnupMatrix

parent, daughter = Isotope(26, "Fe", 56), Isotope(27, "Co", 56)
parent.decay_constant = 1.0
parent.add_decay(DecayLink("beta-", 1.0, 0.0, 1, 0, product=daughter))

matrix = BurnupMatrix([parent, daughter], BurnupConfig(flux=0.0))
matrix.build()
print(matrix.solve([1.0, 0.0], 2.0, method="cram16"))   # [0.1353 0.8647]
```

::::{dropdown} Full script
```{literalinclude} ../../examples/documentation_quickstart.py
:language: python
```
::::

Next: {doc}`first-gui-run` with real nuclear data, or {doc}`../api/scripting` to continue in Python.
