# Architecture and source map

NuMatRx has three layers. Each one only talks to the layer below it, so the numerical core can be used without the GUI and without data files.

```text
 nuclear data          ENDF-6 · MACS tables · TALYS · user JSON/CSV
                                     │
                         NuclearDataProvider          nuclear_data/
                                     │
 calculation             IsotopeBuilder                core/
                                     │
                  Isotope · DecayLink · ReactionLink
                                     │
            NuclearService ──▶ BurnupMatrix ──▶ CRAM / Padé
                   │                      │
                   │                N(t), heat
                   ▼
     RunResult · EqResult · SensitivityResult · ExposureResult
                                     │
 presentation          tables · graphs · exports · sessions      model/
```

## Nuclear data — `nuclear_data/`

| Module | Role |
|---|---|
| `models.py` | dataclasses for decay channels, cross sections, MACS points, isomeric branching |
| `path_holder.py` | `EndfPathHolder`: where the libraries are |
| `endf_reader.py` | ENDF-6 decay (MF=8, MT=457) and neutron data (MF=3, 9, 10) |
| `macs_reader.py` | single- and multi-temperature MACS tables |
| `talys_reader.py` | TALYS cross sections and MACS |
| `user_reader.py` | the user database (`user_db/`) |
| `provider.py` | `NuclearDataProvider`: one interface over all readers, with source priorities |

## Calculation core — `core/`

| Module | Main objects |
|---|---|
| `entities.py` | `Isotope`, `DecayLink`, `ReactionLink`, `Element`, `ChemTable` |
| `registry.py` | `IsotopeBuilder` — data → linked isotopes |
| `burnup.py` | `BurnupConfig`, `BurnupMatrix` — filters, matrix and heat assembly, solving, equilibrium |
| `cram.py` | CRAM-16, adaptive CRAM-16, CRAM-48 |
| `service.py` | `NuclearService` — the working network and all calculation requests from the GUI; `RunResult`, `EqResult` |
| `sensitivity.py` | `SensitivityConfig`, `SensitivityEngine`, `SensitivityResult` |
| `cycle_finder.py` | `CycleAnalyzer`, `IsotopeCycle` |
| `exposure.py` | `ExposureConfig`, `ExposureResult` — time and exposure averaging, mass-number sums, export |
| `session.py` | saving and loading `.kaz` sessions |
| `plotting.py` | Matplotlib helpers for scripts |

`BurnupMatrix` does not read files: it accepts any list of isotope-like objects. This is what makes hand-built networks and unit tests possible.

## Application — `model/`

| Module | Workspace |
|---|---|
| `core.py` | entry point: window, theme, splash screen, panels |
| `GUIcomp.py` | shared widgets, background workers, progress |
| `modelCoreNucleo/` | Periodic Table |
| `modelIsotopeChart/` | Isotope Chart: selection, data settings, matrix build, cycles |
| `modelresults/` | Results: matrix table, manual channels, evolution, equilibrium, sensitivity, saved sessions |
| `exposure_panel.py` | Trajectory averaging panel |
| `modelgraph/` | Graph workspace and the shared averaged-abundance plot |

The GUI never computes physics itself: it sends settings to `NuclearService` and displays the returned result objects. That is why a table and a plot always show the same run, and why plot settings never trigger a recalculation.

## Tests — `tests/`

| File | Covers |
|---|---|
| `test_all.py` | entities, matrix assembly, solver interfaces, synthetic chains |
| `test_cram_adaptive.py`, `test_cram48.py` | solver accuracy, stiff networks, conservation |
| `test_exposure.py`, `test_time_averaging.py` | averaging, aggregation, export, sessions |
| `test_workspace_membership.py` | network membership and manual channels |
| `test_graph_theme.py` | graph mode buttons and themes |

```bash
python -B -m unittest discover -s tests -p "test_*.py"
```

The tests use synthetic networks and need no nuclear data; GUI tests run with an off-screen Qt platform.

## Building this documentation

```bash
python -m pip install -r docs/requirements.txt
python -m sphinx -W --keep-going -b html docs docs/_build/html
```

The API reference imports `core` and `nuclear_data` (NumPy and SciPy are installed for this); Qt, Matplotlib and the `endf` package are mocked, and no nuclear data are read. Read the Docs builds the site from `.readthedocs.yaml`; the GitHub workflow builds it on every push.
