# Tutorial 4: Equilibrium heat versus flux

**You will learn** to compute how the equilibrium energy release of a network depends on the neutron flux, from a script.

The example is `examples/heat_vs_flux.py`. It uses the thirteen-nuclide termination network of {doc}`termination-cycle`, starts from Pb-206 and scans eight fluxes from $10^{14}$ to $10^{28}$ n/cm²/s.

## Run it

```bash
python examples/heat_vs_flux.py
```

The script expects `xsdir/` inside the project folder and the example user database in `examples/user_db/`. It prints a table of flux and equilibrium heat and saves two figures next to the script:

- `heat_density_flux.pdf` — equilibrium heat $Q_\mathrm{eq}$ versus flux;
- `heat_qt.pdf` — heat $Q(t)$ for three fluxes, to check that each run really reaches a plateau.

## How it works

The key call is

```python
from core import BurnupConfig, equilibrium_heat_vs_flux

cfg = BurnupConfig()
cfg.enable_specific_reactions([102])
cfg.set_decay_time_filter("all")
cfg.set_open_boundary(True)

fluxes, heats = equilibrium_heat_vs_flux(isotopes, cfg, N0, np.logspace(14, 28, 8))
```

For each flux the matrix is rebuilt (reaction rates are proportional to $\Phi$), the plateau is found, and the heat release there is computed from every enabled decay and reaction channel. You can also give the plateau times yourself with `t_plateau=` (one value or one per flux).

How the plateau is found depends on the boundary:

- **closed** network — the heat grows towards a steady state; NuMatRx increases the time until the inventories stop changing;
- **open** network — material eventually leaves, so the heat rises, passes a maximum and falls; the maximum is taken as the plateau.

## The same in the application

**Results → Equilibrium**, mode **Auto plateau**, enter the fluxes (`1e14 1e16 1e18 1e20`), press **Calculate Equilibrium**. Plot with **Graph → Equilibrium heat vs flux**, in MeV/s per initial nucleus or, with a material density, in W/cm³.
