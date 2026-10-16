# Sessions and plotting

## Sessions — `core.session`

```{py:module} core.session
```

A session (`.kaz`) stores a finished evolution run, its trajectory average and an equilibrium scan, so that they can be opened again later. It is the format used by **Save…** and **Open…** in the application.

```{py:function} save_session(run, eq, rho, path)

Save results to a file.

:param run: the evolution run; its `exposure_result`, if any, is saved too.
:type run: ~core.service.RunResult
:param eq: an equilibrium scan or `None`.
:type eq: ~core.service.EqResult or None
:param rho: material density used for the W cm⁻³ conversion of heat (g cm⁻³); 0 if not used.
:type rho: float
:param path: output file.
```

```{py:function} load_session(path)

:returns: `(run, eq, rho)`.
:rtype: tuple[~core.service.RunResult, ~core.service.EqResult or None, float]
:raises ValueError: if the file is not a NuMatRx session.
```

```{warning}
Sessions use Python's *pickle* format. Load only files from trusted sources.
```

## Plotting — `core.plotting`

```{py:module} core.plotting
```

Matplotlib helpers for scripts. Each function saves a figure and returns the file name. Time axes are shown in convenient units (seconds to years).

```{py:function} plot_concentrations(names, times, trajectories, filename="concentrations.png", mode="relative", sigma_weights=None, stable_isotopes=None, title="Isotope Concentration Evolution", logy=False, logx=False, min_fraction=1e-30, ymin=1e-31)

Inventory of each nuclide versus time.

:param mode: `"relative"` (fraction of the total), `"absolute"`, or `"sigmaN"` (inventory times cross section; needs `sigma_weights`).
:param stable_isotopes: names drawn as stable nuclides.
:param min_fraction: nuclides that never exceed this value are not drawn.
```

```{py:function} plot_heat(times, heat_values, filename="heat.png", title="Mixture Decay Heat Profile", logy=False, logx=False, ymin=1e-31)

Heat release (MeV s⁻¹ per initial nucleus) versus time.
```

```{py:function} plot_heat_vs_flux(fluxes, heats, filename="heat_vs_flux.png", title="Equilibrium Plateau Heat vs. Neutron Flux", logx=True, logy=True)

Equilibrium heat versus flux, e.g. from {py:func}`~core.burnup.equilibrium_heat_vs_flux`.
```

**Example**

```python
from core import plot_concentrations, plot_heat

plot_concentrations(m.names(), times, traj, filename="conc.png", mode="relative", logx=True, logy=True)
plot_heat(times, m.heat_curve(traj), filename="heat.png", logx=True, logy=True)
```
