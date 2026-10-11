# Python API guide

The GUI delegates calculations to ordinary Python objects. Import them from the repository root; the project is not documented as an installed PyPI package. The public names below refer to the current source interfaces and can change between revisions.

## Main entry points

| Object / function | Purpose |
|---|---|
| `core.entities.Isotope(Z, X, A, meta=None)` | A ground or metastable nuclide with outgoing links |
| `DecayLink(mode, branch, Q_MeV, dz, da, rfs=0, product=None)` | Decay channel linked to its daughter |
| `ReactionLink(mt, name, sigma_barn, ..., product=None)` | Neutron channel with effective cross section |
| `BurnupConfig(flux=0.0)` | Flux, channel filters, and boundary configuration |
| `BurnupMatrix(isotopes, config)` | Matrix assembly and propagation |
| `matrix.build()` | Assemble matrices from the current linked objects |
| `matrix.names()` | Ordered names corresponding to vector entries |
| `matrix.solve(N0, t_sec, method='cram16')` | Propagate a constant matrix from the initial vector |
| `core.exposure.average_run(run, config)` | Average a saved service result |
| `core.session.save_session(run, eq, rho, path)` | Save a result archive |
| `core.session.load_session(path)` | Return stored run, equilibrium result, and density |

Always align `N0` with `matrix.names()`. Rates are not inferred from an isotope label when you construct entities manually. See the [complete data-free example](quickstart.md).

## Service-level evolution

Once a `NuclearService` instance has been initialized with data and a working network, its `run_evolution` method accepts an initial-label dictionary, final time, flux, energy, solver, filters, boundaries, and output-grid options. A representative call is:

```python
# svc must already contain the intended data provider and selected network.
run = svc.run_evolution(
    {"Fe-56": 1.0}, 1e15,
    flux=2.5e16, energy_eV=30000.0,
    method="cram16_adaptive", mt_filter=[102],
    hl_preset="all", n_points=800, t_start_s=1e-6,
    open_boundary_mts=[102], target_labels=None,
)
```

This snippet configures a calculation; it is not standalone network construction. `n_points` changes the saved grid. The per-MT boundary list overrides the global flag for unresolved reaction daughters. See the boundary discussion in [Methods](methods.md#network-boundaries-and-scientific-validation).

## Average an existing RunResult

```python
from core.exposure import ExposureConfig, average_run, export_exposure

config = ExposureConfig(mode="exposure", tau0=0.3)
result = average_run(run, config)
export_exposure(result, "exposure_average.csv")
print(result.diagnostics)
```

Time modes use `mode="time_uniform"` with `start_s` and `end_s`, or `mode="time_exponential"` with `mean_time_s`. Exposure averaging requires a positive fixed flux. Inspect `result.warnings` and retain source metadata.

## Development checks

```bash
python -m unittest discover -s tests -p "test_cram*.py"
python examples/documentation_quickstart.py
python -m sphinx -W --keep-going -b html docs docs/_build/html
```

Broader GUI tests may depend on installed Qt and rendering tools. Numerical verification and documentation generation do not require distributing private nuclear libraries. Documentation uses explicit interface descriptions and runnable examples, so the Sphinx build does not import or launch the GUI.
