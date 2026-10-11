# Tutorial 1: A decay chain in Python

**You will learn** how a network is made of `Isotope` objects, how to build and solve the burnup matrix, and how to check a solver against an exact solution. No nuclear library is needed: we enter the half-lives by hand.

## The model

The fission product Sr-90 decays into Y-90, which decays into stable Zr-90:

$$
{}^{90}\mathrm{Sr} \xrightarrow[\;28.79\ \mathrm{y}\;]{\beta^-} {}^{90}\mathrm{Y} \xrightarrow[\;64.05\ \mathrm{h}\;]{\beta^-} {}^{90}\mathrm{Zr}.
$$

Starting from pure Sr-90, the exact (Bateman) solution for Y-90 is

$$
N_2(t) = N_1(0)\,\frac{\lambda_1}{\lambda_2 - \lambda_1}\left(e^{-\lambda_1 t} - e^{-\lambda_2 t}\right).
$$

## Build the network

```python
import numpy as np
from core.entities import Isotope, DecayLink
from core.burnup import BurnupConfig, BurnupMatrix

YEAR, HOUR, DAY = 3.15576e7, 3600.0, 86400.0

sr, y, zr = Isotope(38, "Sr", 90), Isotope(39, "Y", 90), Isotope(40, "Zr", 90)
sr.half_life_s = 28.79 * YEAR
y.half_life_s = 64.05 * HOUR
sr.decay_constant = np.log(2) / sr.half_life_s
y.decay_constant = np.log(2) / y.half_life_s

# DecayLink(mode, branch, Q_MeV, dZ, dA, product=daughter)
sr.add_decay(DecayLink("beta-", 1.0, 0.546, 1, 0, product=y))
y.add_decay(DecayLink("beta-", 1.0, 2.280, 1, 0, product=zr))

matrix = BurnupMatrix([sr, y, zr], BurnupConfig(flux=0.0))
matrix.build()
print(matrix.names())        # ['Sr-90', 'Y-90', 'Zr-90']
```

The order of `matrix.names()` is the order of every inventory vector.

## Solve and compare

```python
N0 = np.array([1.0, 0.0, 0.0])
l1, l2 = sr.decay_constant, y.decay_constant

for t in (1 * DAY, 30 * DAY, 10 * YEAR):
    exact = l1 / (l2 - l1) * (np.exp(-l1 * t) - np.exp(-l2 * t))
    for method in ("pade", "cram16", "cram16_adaptive", "cram48"):
        N = matrix.solve(N0, t, method=method)
        print(f"t={t:9.3e} s  {method:16s} Y-90={N[1]:.6e}  "
              f"rel. error={abs(N[1] - exact) / exact:.0e}")
```

All four solvers reproduce the exact value to about $10^{-14}$ relative error. The sum $N_1+N_2+N_3$ stays exactly 1, because the chain is closed.

## Secular equilibrium

After about ten Y-90 half-lives (a month), Y-90 is in equilibrium with its long-lived parent, and the ratio is set by the decay constants:

```python
N = matrix.solve(N0, 30 * DAY)
print(N[1] / N[0], l1 / (l2 - l1))     # both ≈ 2.538e-4
```

## Heat release

Each decay link carries its energy `Q_MeV`. The heat release rate at any time is

```python
print(matrix.heat_release(N), "MeV/s per initial Sr-90 nucleus")
```

## A whole trajectory

```python
times = np.logspace(3, 10, 200)                     # 1000 s … 300 years
times, trajectory = matrix.evolve(N0, times, method="cram16")
heat = matrix.heat_curve(trajectory)
```

`trajectory` has one row per time and one column per nuclide. Plotting helpers are described in {doc}`../api/scripting`.

## Time average

```python
from core.exposure import ExposureConfig, average_exposure

grid = np.linspace(0.0, 30 * DAY, 2001)
traj = [matrix.solve(N0, float(t)) for t in grid]
result = average_exposure(
    matrix.names(), grid, traj, 0.0,
    ExposureConfig(mode="time_uniform", start_s=0.0, end_s=30 * DAY))
print(dict(zip(result.names, result.mean)))
```

`result.warnings` notes that no capture cross sections are present — expected here, since this network has no neutron reactions.

A ready-made test of the same kind, with all checks built in, is `examples/documentation_quickstart.py` ({doc}`../getting-started/first-calculation`).

## Exercises

1. Plot $N_2/N_1$ over time and watch it approach $\lambda_1/(\lambda_2-\lambda_1)$.
2. Add a branch: let Y-90 decay with branch 0.9 to Zr-90 and 0.1 to a new nuclide.
3. Halve the number of points in the averaging grid and see how the average changes.
