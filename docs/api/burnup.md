# Burnup matrix and solvers

{py:class}`~core.burnup.BurnupConfig` says *which* channels enter the matrix and under *which* conditions; {py:class}`~core.burnup.BurnupMatrix` assembles the matrix for a list of isotopes and solves $d\mathbf N/dt = \mathbf A\mathbf N$. The CRAM functions in `core.cram` do the numerical work. Theory: {doc}`../theory/network-equations`, {doc}`../theory/solvers`.

| Object | Purpose |
|---|---|
| {py:class}`~core.burnup.BurnupConfig` | flux, reaction (MT) filter, decay-mode and half-life filters, boundaries, manual decays |
| {py:class}`~core.burnup.BurnupMatrix` | matrix assembly, evolution, equilibrium, heat, export |
| {py:func}`~core.burnup.equilibrium_heat_vs_flux` | equilibrium heat for a list of fluxes |
| {py:func}`~core.cram.cram16_step`, {py:func}`~core.cram.adaptive_cram16`, {py:func}`~core.cram.cram48_step` | matrix-exponential solvers |

## Configuration and matrix — `core.burnup`

```{py:module} core.burnup
```

::::{py:class} BurnupConfig(flux=0.0)

Calculation settings. Create one, adjust it with the setters, then pass it to {py:class}`BurnupMatrix`.

:param flux: neutron flux in n cm⁻² s⁻¹; `0` means decay only.
:type flux: float

```{py:attribute} flux
:type: float

Neutron flux, n cm⁻² s⁻¹.
```

```{py:attribute} manual_decay_links
:type: list[dict]

Decays added by hand. Each dict has the keys `parent`, `daughter` (`""` for a sink), `mode`, `half_life_s` and `branch`. A manual link replaces the library branch with the same parent and mode, and is not affected by the decay filters.
```

**Reactions**

```{py:method} enable_all_reactions()

Accept every MT channel (default).
```

```{py:method} enable_specific_reactions(mt_list)

Accept only the listed MT numbers, e.g. `[102]` for (n,γ) only.
```

```{py:method} is_reaction_allowed(mt)

:rtype: bool
```

**Decays**

```{py:method} set_decay_mode_filter(modes)

Accept only the listed decay modes, e.g. `["beta-", "alpha"]`; `None` accepts all.
```

```{py:method} is_decay_mode_allowed(mode)

:rtype: bool
```

```{py:method} set_decay_time_filter(preset="all")

Keep only decays whose half-life does not exceed the preset limit.

:param preset: `"all"`, `"yearly"` (3.156 × 10⁷ s), `"daily"` (86 400 s), `"hourly"` (3600 s), `"minute"` (60 s) or `"second"` (1 s).
:raises ValueError: for an unknown preset.
```

```{py:method} set_decay_time_range(min_s=0.0, max_s=None)

Keep only decays with `min_s <= T½ <= max_s` (seconds); `max_s=None` has no upper limit.
```

```{py:method} is_decay_allowed(half_life_s)

:returns: whether a decay with this half-life passes the filter; stable nuclides (`None`) always pass.
:rtype: bool
```

**Boundaries** — what happens to a neutron reaction whose product is not in the network. Decays leaving the network are always kept as sinks.

```{py:method} set_open_boundary(open_b=True)

Global setting for all MT channels. `True`: such reactions are sinks (material leaves). `False` (default): such reactions are switched off.
```

```{py:method} set_open_boundary_mts(mts)

Per-channel setting: only the listed MT numbers are open, all others are closed. `None` returns to the global setting.
```

```{py:method} is_mt_boundary_open(mt)

:rtype: bool
```
::::

::::{py:class} BurnupMatrix(isotopes, config)

The burnup matrix of a network and its solution. It does not read files: any objects with the interface of {py:class}`~core.entities.Isotope` can be used.

:param isotopes: the network; its order defines the order of all vectors.
:type isotopes: list[~core.entities.Isotope]
:param config: calculation settings; `config.flux` is read at construction.
:type config: BurnupConfig

```{py:attribute} matrix_A
:type: numpy.ndarray | None

The full matrix $\mathbf A$ (s⁻¹), shape `(n, n)`, available after {py:meth}`build`. Column *j* belongs to parent *j*.
```

```{py:attribute} matrix_decay
:type: numpy.ndarray | None

Decay part of $\mathbf A$.
```

```{py:attribute} matrix_rxn
:type: numpy.ndarray | None

Neutron-reaction part of $\mathbf A$.
```

```{py:attribute} matrix_heat
:type: numpy.ndarray | None

Diagonal matrix of heat coefficients (MeV s⁻¹ per nucleus of each parent).
```

```{py:attribute} missing
:type: list[dict]

Reaction channels without a cross section found during {py:meth}`build`.
```

**Assembly**

```{py:method} build(missing_callback=None)

Assemble `matrix_A`, `matrix_decay`, `matrix_rxn` and `matrix_heat` from the enabled channels. Reaction rates are $10^{-24}\,\Phi\,\sigma$ with σ in barn.

:param missing_callback: called with an info dict for each reaction without a cross section; it may return a value in barn to use instead. Without a callback, such channels are listed in {py:attr}`missing`.
:type missing_callback: callable or None
:returns: the matrix `matrix_A`.
```

```{py:method} validate()

Quick structural check: non-positive diagonal and non-positive column sums.

:returns: `False` if the matrix is not built or the check fails.
:rtype: bool
```

```{py:method} names()

:returns: isotope names in matrix order. Use it to build and read inventory vectors.
:rtype: list[str]
```

**Evolution**

```{py:method} solve(N0, t_sec, method="cram16")

Inventory after a time `t_sec` with constant conditions: $\mathbf N(t) = e^{\mathbf A t}\mathbf N_0$.

:param N0: initial inventory, length `n`, in matrix order.
:type N0: array_like
:param t_sec: time in seconds (finite, non-negative).
:type t_sec: float
:param method: `"cram16"`, `"cram16_adaptive"`, `"cram48"`, `"pade"`, `"taylor"` or `"bdf"`.
:type method: str
:returns: inventory at `t_sec`.
:rtype: numpy.ndarray
:raises RuntimeError: if {py:meth}`build` has not been called.
:raises ValueError: for an unknown method or an invalid time.
```

```{py:method} evolve(N0, times, method="cram16")

Solve for a list of times. Each time is computed directly from `N0`, so errors do not accumulate.

:returns: `(times, trajectories)` where `trajectories[k]` is the inventory at `times[k]`.
:rtype: tuple[list, list[numpy.ndarray]]
```

**Heat**

```{py:method} heat_release(N)

:returns: total heat release for inventory `N`, MeV s⁻¹ (per unit of initial inventory).
:rtype: float
```

```{py:method} heat_curve(trajectories)

:returns: {py:meth}`heat_release` for every vector of a trajectory.
:rtype: list[float]
```

**Equilibrium**

```{py:method} solve_equilibrium(N0, method="cram16", rtol=1e-4, t_start=None, t_max=1e25, max_steps=60)

Find the plateau composition: the time is multiplied by 3 until the largest relative change of the inventory is below `rtol`. By default the search starts at about ten times the slowest process time of the matrix.

:returns: `(N_eq, t_reached)`. If no plateau is found before `t_max`, the last vector and `t_max` are returned.
:rtype: tuple[numpy.ndarray, float]
```

```{py:method} find_plateau(N0, method="cram16", n_scan=80, t_min=1e-3, t_max=1e25)

Scan heat release on a logarithmic grid and return the time of its maximum. Useful for open networks, where the heat rises, peaks and falls.

:returns: `(t_plateau, Q_plateau)` in s and MeV s⁻¹.
:rtype: tuple[float, float]
```

```{py:method} equilibrium_heat(N0, method="cram16", t_plateau=None, n_scan=80, t_min=1e-3, t_max=1e25)

Heat release at the plateau, MeV s⁻¹. Closed networks use {py:meth}`solve_equilibrium`; open networks use {py:meth}`find_plateau`. A given `t_plateau` (s) overrides the search.

:rtype: float
```

**Export**

```{py:method} export_txt(filename, mode="total")

Write the matrix as a tab-separated table with isotope names as row and column headers.

:param mode: `"total"` (`matrix_A`), `"decay"` or `"rxn"`.
```

```{py:method} export_evolution_txt(filename, times, trajectories)

Write a trajectory: first column `Time_sec`, then one column per isotope.
```

**Example**

```python
import numpy as np
from core import BurnupConfig, BurnupMatrix

cfg = BurnupConfig(flux=1e14)
cfg.enable_specific_reactions([102])
cfg.set_decay_time_filter("all")
cfg.set_open_boundary_mts([102])

m = BurnupMatrix(isotopes, cfg)
m.build()
N0 = np.zeros(len(m.names())); N0[m.names().index("Pb-206")] = 1.0
times, traj = m.evolve(N0, np.logspace(6, 14, 100), method="cram16_adaptive")
heat = m.heat_curve(traj)
N_eq, t_eq = m.solve_equilibrium(N0)
```
::::

```{py:function} equilibrium_heat_vs_flux(isotopes, config_template, N0, fluxes, method="cram16", n_scan=80, t_plateau=None)

Equilibrium heat release for each flux. For every flux a copy of `config_template` gets that flux, the matrix is rebuilt and {py:meth}`BurnupMatrix.equilibrium_heat` is evaluated.

:param fluxes: fluxes in n cm⁻² s⁻¹.
:param t_plateau: `None` (automatic), one time in s, or a list with one time per flux.
:returns: `(fluxes, heats)` with heats in MeV s⁻¹.
:rtype: tuple[list[float], list[float]]
:raises ValueError: if a list `t_plateau` has a different length from `fluxes`.
```

## Solvers — `core.cram`

```{py:module} core.cram
```

These functions take the matrix and a vector directly. Normally you call them through {py:meth}`BurnupMatrix.solve <core.burnup.BurnupMatrix.solve>`.

```{py:function} cram16_step(matrix, vector, step)

One CRAM step of order 16 (eight complex poles, partial-fraction form) over the time `step`. Uses sparse LU factorisations; no error control.

:returns: the propagated vector.
:rtype: numpy.ndarray
```

```{py:function} adaptive_cram16(matrix, initial, duration, *, rtol=1e-9, atol=1e-14, max_attempts=4096, should_cancel=None)

CRAM-16 with step-size control by step doubling. A step is accepted when one full step and two half steps agree within the tolerances, no value is significantly negative, and the total inventory is conserved (closed networks) or does not grow (networks with losses). Values are never clipped or renormalised.

:param rtol: relative tolerance, per component.
:param atol: absolute tolerance, relative to the initial total inventory.
:param should_cancel: optional callable; returning `True` stops the calculation.
:raises ValueError: for an invalid matrix, vector, duration or tolerance.
:raises RuntimeError: if the step refinement does not converge or is cancelled.
:rtype: numpy.ndarray
```

```{py:function} cram48_step(matrix, initial, duration)

One step of order 48 in incomplete partial-fraction form (24 poles applied one after another). An independent implementation, useful to cross-check CRAM-16.

:rtype: numpy.ndarray
```
