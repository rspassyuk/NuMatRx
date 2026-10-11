# Scripting with Python

Everything the application does is available from Python: the GUI is a thin layer over the packages `core` (network and calculations) and `nuclear_data` (file readers). Use scripts for parameter scans, batch runs and notebooks.

Run your scripts from the repository folder, or add it to `sys.path`:

```python
import sys
sys.path.insert(0, "/path/to/NuMatRx")
```

There are three levels, from the most explicit to the most convenient.

## Level 1: a network built by hand

No data files are needed. You create the nuclides and their links yourself.

```python
import numpy as np
from core import Isotope, DecayLink, ReactionLink, BurnupConfig, BurnupMatrix

co59, co60, ni60 = Isotope(27, "Co", 59), Isotope(27, "Co", 60), Isotope(28, "Ni", 60)
co60.half_life_s = 5.2714 * 3.15576e7
co60.decay_constant = np.log(2) / co60.half_life_s

co59.add_reaction(ReactionLink(102, "(n,g)", 37.2, product=co60))   # σ in barn
co60.add_decay(DecayLink("beta-", 1.0, 2.824, 1, 0, product=ni60))  # Q in MeV

matrix = BurnupMatrix([co59, co60, ni60], BurnupConfig(flux=1e14))
matrix.build()
N = matrix.solve([1.0, 0.0, 0.0], 3.15576e7)       # one year
print(dict(zip(matrix.names(), N)))
# {'Co-59': 0.889, 'Co-60': 0.104, 'Ni-60': 0.0071}
```

This is cobalt activation: one year at $10^{14}$ n/cm²/s turns about 11 % of Co-59 into Co-60, part of which has already decayed to Ni-60.

`BurnupMatrix` accepts any objects with the same attributes as `Isotope`, so you can plug in your own data structures.

## Level 2: a network from nuclear data

`NuclearDataProvider` reads the libraries; `IsotopeBuilder` turns them into linked `Isotope` objects.

```python
from core import IsotopeBuilder, BurnupConfig, BurnupMatrix
from nuclear_data import EndfPathHolder, NuclearDataProvider

EndfPathHolder.init_xsdir("xsdir")
nd = NuclearDataProvider(
    dec_dir=EndfPathHolder.set_DEFAULT_DEC_DIR("ENDFB-VIII.0"),
    neu_dir=EndfPathHolder.set_DEFAULT_NEU_DIR("ENDFB-VIII.0"),
    macs_file=EndfPathHolder.set_DEFAULT_MACS_DIR("Endfb7"), macs_lib="Endfb7",
    endfb71_macs_dir=str(EndfPathHolder.get_ENDFB71_MACS_DIR()),
    eaf2010_macs_dir=str(EndfPathHolder.get_EAF2010_MACS_DIR()),
    talys_dir=str(EndfPathHolder.get_TALYS_DIR()),
    macs_priority=["user", "rawmacs", "endfb71", "eaf2010", "talys", "endf_computed"],
)

specs = [(82, "Pb", 206), (82, "Pb", 207), (82, "Pb", 208), (82, "Pb", 209),
         (83, "Bi", 209), (83, "Bi", 210), (84, "Po", 210)]
builder = IsotopeBuilder(nd)
isotopes = builder.build_range(specs, E_eV=30_000.0, mt_filter=[102], prefer_macs=True)
builder.print_report()            # what was found, from which source, what is missing

cfg = BurnupConfig(flux=1e14)
cfg.enable_specific_reactions([102])     # MT filter
cfg.set_decay_time_filter("all")         # half-life preset
cfg.set_open_boundary_mts([102])         # captures leaving the network are sinks

matrix = BurnupMatrix(isotopes, cfg)
matrix.build()
```

`prefer_macs=True` selects astrophysics mode (MACS at $kT$ = `E_eV`); `False` selects reactor mode (σ(E) at `E_eV`).

### Solve, trajectories, heat

```python
names = matrix.names()
N0 = np.zeros(len(names)); N0[names.index("Pb-206")] = 1.0

N = matrix.solve(N0, 1e13, method="cram16_adaptive")     # one time
times, traj = matrix.evolve(N0, np.logspace(8, 14, 100))  # many times
heat = matrix.heat_curve(traj)                            # MeV/s per initial nucleus
N_eq, t_eq = matrix.solve_equilibrium(N0)                 # plateau
```

Methods: `"cram16"`, `"cram16_adaptive"`, `"cram48"`, `"pade"`, and for experiments `"taylor"`, `"bdf"`.

### Export and plots

```python
matrix.export_txt("matrix.txt", mode="total")
matrix.export_evolution_txt("evolution.txt", times, traj)

from core import plot_concentrations, plot_heat
plot_concentrations(names, times, traj, filename="conc.png", mode="relative", logx=True, logy=True)
plot_heat(times, heat, filename="heat.png", logx=True, logy=True)
```

## Level 3: the application's service

`NuclearService` is what the GUI uses. It finds `xsdir` and `user_db` by itself, keeps the working network, and returns the same result objects that the application shows and saves.

```python
from core.service import NuclearService

svc = NuclearService()
svc.init(".")                       # project folder; finds xsdir inside or next to it
svc.build_universe_from_labels(
    ["Pb-206", "Pb-207", "Pb-208", "Pb-209", "Pb-210", "Bi-209", "Bi-210", "Po-210"],
    E_eV=30_000.0, mt_filter=[102], prefer_macs=True)

run = svc.run_evolution({"Pb-206": 1.0}, 1e14,
                        flux=1e14, energy_eV=30_000.0,
                        method="cram16", mt_filter=[102])
print(run.final())                  # {'Pb-206': 0.0364, ..., 'Bi-209': 0.1479, ...}
```

`run` is a `RunResult` with `names`, `times` (400 points), `trajectories` and `heat`. Other options of `run_evolution`: `n_points`, `t_start_s`, `hl_preset`, `decay_mode_filter`, `open_boundary_mts`, `target_labels`.

### Averaging

```python
from core.exposure import ExposureConfig, average_run, mass_values, export_exposure

avg = average_run(run, ExposureConfig(mode="exposure", tau0=0.3))
A, N_A = mass_values(avg)                       # sums over mass number
export_exposure(avg, "average.csv")
print(avg.coverage, avg.tail, avg.warnings)
```

Modes: `"exposure"` (`tau0` in mbarn⁻¹), `"time_exponential"` (`mean_time_s`), `"time_uniform"` (`start_s`, `end_s`).

### Sensitivity

```python
from core.sensitivity import SensitivityConfig, SensitivityEngine

cfg = SensitivityConfig(
    initial_by_label={"Pb-206": 1.0},
    target_kind="concentration", target_label="Bi-209",
    eval_mode="plateau", types=["sigma"],
    flux=1e14, energy_eV=30_000.0, mt_filter=[102], prefer_macs=True)
result = SensitivityEngine(svc).run(cfg)
for row in result.rows[:4]:
    print(f"{row.parameter:15s} S = {row.S:+.3f}")
```

```text
Bi-209 (n,γ)    S = -0.852
Pb-208 (n,γ)    S = +0.756
Pb-207 (n,γ)    S = +0.060
Pb-206 (n,γ)    S = +0.036
```

`types` can contain `"sigma"`, `"halflife"`, `"flux_energy"` and `"library"`.

### Sessions

```python
from core.session import save_session, load_session

save_session(run, None, 0.0, "my_run.kaz")      # run, equilibrium result, density
run, eq, rho = load_session("my_run.kaz")
```

## Cycles

```python
from core import CycleAnalyzer

analyzer = CycleAnalyzer(isotopes)
for c in analyzer.find_all_cycles(max_length=10):
    print(" → ".join(c.isotope_names))
```

## Examples in the repository

| Script | What it shows |
|---|---|
| `examples/documentation_quickstart.py` | a synthetic chain; all solvers checked against the exact solution; no data needed |
| `examples/sprocess_termination.py` | the Pb–Bi–Po network: links, cycles, evolution, exports and plots |
| `examples/heat_vs_flux.py` | equilibrium heat over a grid of fluxes |

The complete list of classes and functions is in {doc}`reference`.
