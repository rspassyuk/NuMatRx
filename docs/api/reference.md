# API reference

This reference describes the Python interface of NuMatRx: every public class, its parameters and attributes, and what each method returns. For a guided introduction with complete examples, start with {doc}`scripting`.

## Package map

NuMatRx has two Python packages. The GUI (`model/`) is built on top of them and is not part of the public API.

```text
nuclear_data/            reading nuclear data from files          → Nuclear data
core/
├── entities, registry   nuclides, links, building a network      → Network
├── burnup, cram         burnup matrix and solvers                → Burnup matrix and solvers
├── service              the high-level facade used by the GUI    → Application service
├── exposure             time and exposure averaging              → Analysis
├── sensitivity          one-at-a-time sensitivity                → Analysis
├── cycle_finder         closed reaction cycles                   → Analysis
└── session, plotting    saving results, figures                  → Sessions and plotting
```

## How the classes work together

```text
 NuclearDataProvider ──▶ IsotopeBuilder ──▶ [Isotope, DecayLink, ReactionLink]
   (nuclear_data)          (registry)                    │
                                                         ▼
                              BurnupConfig ──▶ BurnupMatrix ──▶ N(t), heat
                                                         │
 NuclearService ── wraps all of the above ──▶ RunResult / EqResult
                                                         │
                     average_run · SensitivityEngine · CycleAnalyzer · save_session
```

There are three ways in, from the most explicit to the most convenient:

| Level | Entry point | You provide |
|---|---|---|
| hand-built network | {py:class}`~core.entities.Isotope`, {py:class}`~core.burnup.BurnupMatrix` | decay constants and cross sections yourself |
| network from data | {py:class}`~nuclear_data.provider.NuclearDataProvider`, {py:class}`~core.registry.IsotopeBuilder` | paths to the libraries and a list of nuclides |
| application service | {py:class}`~core.service.NuclearService` | the project folder; results come back as {py:class}`~core.service.RunResult` |

## Conventions

| Topic | Convention |
|---|---|
| Inventory vectors | ordered as {py:meth}`BurnupMatrix.names() <core.burnup.BurnupMatrix.names>`; units are those of the initial inventory |
| Time | seconds |
| Flux | neutrons cm⁻² s⁻¹ |
| Energy arguments | `E_eV`, `energy_eV` in eV; `kT_keV` in keV (30 keV = `30000.0` eV) |
| Cross sections | barn in links and matrices; millibarn in MACS tables ({py:class}`~nuclear_data.models.MacsPoint`) |
| Heat | MeV s⁻¹ per unit of initial inventory |
| Nuclide labels | `"Pb-206"`, `"Bi-210m1"`; tuples `(Z, "Pb", A)` or `(Z, "Pb", A, meta)` |
| Reaction channels | ENDF MT numbers: 102 (n,γ), 103 (n,p), 107 (n,α), 16 (n,2n), 18 fission |
| Decay modes | `"beta-"`, `"ec/beta+"`, `"it"`, `"alpha"`, `"n"`, `"sf"`, `"p"` |

## Pages

```{toctree}
:maxdepth: 2

network
burnup
service
analysis
nuclear-data
io
```
