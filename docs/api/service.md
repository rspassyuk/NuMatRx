# Application service

{py:class}`~core.service.NuclearService` is the layer the desktop application uses. It finds the data, keeps the working network, assembles matrices and returns result objects. In scripts it is the shortest way to reproduce what the GUI does.

| Object | Purpose |
|---|---|
| {py:class}`~core.service.NuclearService` | data discovery, working network, evolution, equilibrium, sensitivity |
| {py:class}`~core.service.RunResult` | result of an evolution run |
| {py:class}`~core.service.EqResult` | result of an equilibrium scan |
| {py:func}`~core.service.init_service`, {py:func}`~core.service.get_service` | the shared service instance of the application |

```{py:module} core.service
```

::::{py:class} NuclearService()

High-level interface over `nuclear_data` and `core`. Create it, call {py:meth}`init`, build a network, then run calculations.

**Set-up and data**

```{py:method} init(project_root, decay_library="ENDFB-VIII.0", neutron_library="ENDFB-VIII.0", macs_library="Endfb7", progress=None)

Find `xsdir/` (inside `project_root` or next to it) and `user_db/`, and create the data provider with every source found.

:param project_root: the NuMatRx folder.
:param progress: optional callback `progress(fraction, message)`.
```

```{py:property} initialized
:type: bool

`True` after a successful {py:meth}`init`.
```

```{py:method} info()

:returns: a summary: libraries in use, `xsdir` path, whether the `endf` package is available.
:rtype: dict
```

```{py:method} decay_libraries()

:returns: ENDF-6 libraries found in `xsdir/endf-6`.
:rtype: list[str]
```

```{py:method} switch_decay_library(library)

Use another decay library; the working network is rebuilt on the next request.
```

```{py:method} set_dec_priority(libs)

Order of decay sources, e.g. `["user", "endf6"]`.
```

```{py:method} set_macs_priority(libs)

Order of MACS sources, e.g. `["user", "rawmacs", "endfb71", "eaf2010", "talys", "endf_computed"]`.
```

**Reading data for one nuclide** (used by the Periodic Table workspace)

```{py:method} read_decay(library, Z, X, A, meta=None)

:returns: half-life and decay channels from one library, or `None`.
:rtype: dict or None
```

```{py:method} read_neutron(library, Z, X, A, meta=None)

:returns: one dict per MT: channel, σ(E) summary, reaction Q, isomeric branching, MACS at 30 keV.
:rtype: list[dict]
```

```{py:method} read_macs_sources(Z, X, A, meta=None)

:returns: all MACS values available in `xsdir/MACS` for this nuclide, grouped by source.
:rtype: dict
```

```{py:method} scan_isotopes_for_element(library, Z, X)

:returns: `(A, meta)` pairs available for an element in a library.
:rtype: list[tuple]
```

**The working network**

```{py:method} build_universe(z_from=80, z_to=84, n_from=None, n_to=None, E_eV=30000.0, mt_filter=None, prefer_macs=False, progress=None)

Build and link all nuclides in a window of the chart: `z_from <= Z <= z_to`, optionally `n_from <= N <= n_to`. Excluded nuclides are skipped. The result is cached for identical arguments.

:param E_eV: neutron energy or kT in eV.
:param prefer_macs: `True` for astrophysics mode (MACS).
:returns: the working network.
:rtype: list[~core.entities.Isotope]
:raises RuntimeError: if the service is not initialised.
```

```{py:method} build_universe_from_labels(labels, E_eV=30000.0, mt_filter=None, prefer_macs=False, progress=None)

Build the network from labels such as `["Tl-206", "Pb-207", "Pb-208"]`. Ranges `"Tl206..Tl216"` are expanded.

:rtype: list[~core.entities.Isotope]
```

```{py:method} edit_workspace_isotopes(add_labels=(), remove_labels=())

Add or remove nuclides of the working network without changing the channel filters.
```

```{py:method} get_universe(default_range=(80, 84))

:returns: the current network; on first access a default Z window is built.
:rtype: list[~core.entities.Isotope]
```

```{py:method} universe_labels()

:returns: names of the current network.
:rtype: list[str]
```

```{py:method} count_specs(z_from, z_to, n_from=None, n_to=None)

:returns: how many nuclides a window would contain (fast, no data are read).
:rtype: int
```

```{py:method} minimal_subnetwork(source_labels, target_labels, mt_filter=None)

The nuclides lying on at least one path from a source to a target: reachable forward from the sources and backward from the targets. Solving this smaller network gives the same target inventories.

:rtype: list[~core.entities.Isotope]
```

Excluded nuclides are managed with `get_excluded()`, `is_excluded(za)`, `add_excluded(za)`, `remove_excluded(za)`, `set_excluded(zas)` and `clear_excluded()`, where `za` is a `(Z, A)` tuple.

**Calculations**

```{py:method} build_matrix(flux=0.0, energy_eV=30000.0, mt_filter=None, decay_mode_filter=None, open_boundary=False, open_boundary_mts=None, hl_preset="all", isotopes=None, manual_decay_links=None, progress=None)

Assemble a {py:class}`~core.burnup.BurnupMatrix` over the working network (or over `isotopes`). The arguments map to {py:class}`~core.burnup.BurnupConfig`; `open_boundary_mts` overrides `open_boundary`.

:rtype: ~core.burnup.BurnupMatrix
```

```{py:method} run_evolution(initial_by_label, t_end_s, flux=0.0, energy_eV=30000.0, method="cram16", mt_filter=None, decay_mode_filter=None, hl_preset="all", n_points=400, t_start_s=1e-6, open_boundary=False, open_boundary_mts=None, target_labels=None, progress=None, should_cancel=None)

Build the matrix and solve it on a grid of `n_points` times: zero plus a logarithmic grid from `t_start_s` to `t_end_s`.

:param initial_by_label: initial inventory, e.g. `{"Fe-56": 1.0}`; all other nuclides start at zero.
:type initial_by_label: dict[str, float]
:param t_end_s: end time, s.
:param flux: n cm⁻² s⁻¹.
:param method: solver name, see {py:meth}`BurnupMatrix.solve <core.burnup.BurnupMatrix.solve>`.
:param target_labels: if given, only the {py:meth}`minimal_subnetwork` leading to these nuclides is solved.
:param should_cancel: callable; returning `True` stops the run.
:rtype: RunResult
```

```{py:method} run_equilibrium_scan(initial_by_label, flux_list, time_list, energy_eV=30000.0, method="cram16", mt_filter=None, decay_mode_filter=None, hl_preset="all", open_boundary=False, open_boundary_mts=None, progress=None, should_cancel=None)

For each flux `flux_list[i]`, irradiate from the initial inventory for `time_list[i]` seconds and record the inventory and heat.

:rtype: EqResult
```

```{py:method} run_equilibrium_auto(initial_by_label, flux_list, energy_eV=30000.0, method="cram16", mt_filter=None, decay_mode_filter=None, hl_preset="all", open_boundary=False, open_boundary_mts=None, progress=None, should_cancel=None)

Like {py:meth}`run_equilibrium_scan`, but the time for each flux is found with {py:meth}`BurnupMatrix.solve_equilibrium <core.burnup.BurnupMatrix.solve_equilibrium>`.

:rtype: EqResult
```

```{py:method} run_sensitivity(config, progress=None, should_cancel=None)

Run a one-at-a-time sensitivity analysis.

:param config: see {py:class}`~core.sensitivity.SensitivityConfig`.
:rtype: ~core.sensitivity.SensitivityResult
```

```{py:method} set_manual_decay_links(links)

Store manual decay links (same dict format as {py:attr}`BurnupConfig.manual_decay_links <core.burnup.BurnupConfig.manual_decay_links>`); they are added to every following {py:meth}`build_matrix`.
```

```{py:method} get_manual_decay_links()

:rtype: list[dict]
```

**Labels**

```{py:method} parse_label(label)
:staticmethod:

`"Pb-206"` → `(82, "Pb", 206, None)`; `"U-235m1"` → `(92, "U", 235, 1)`; `None` if the label cannot be parsed.
```

```{py:method} expand_label_token(token)
:staticmethod:

`"Tl206..Tl208"` → `["Tl-206", "Tl-207", "Tl-208"]`; a plain label `"Pb-206"` → `["Pb-206"]`.
```

```{py:method} normalize_label(label)
:classmethod:

Canonical form of a label, matching {py:attr}`Isotope.name <core.entities.Isotope.name>`.
```

```{py:method} find_isotope(label)

:returns: the isotope of the working network with this label, or `None`.
```

The remaining public methods (`chart_nuclides`, `reachable_cells`, `chart_decay_modes`, the `register_*_callback` methods and `set_theme`) serve the GUI.

**Example**

```python
from core.service import NuclearService

svc = NuclearService()
svc.init(".")
svc.build_universe_from_labels(["Pb-206", "Pb-207", "Pb-208", "Pb-209", "Bi-209", "Bi-210", "Po-210"],
                               E_eV=30_000.0, mt_filter=[102], prefer_macs=True)
run = svc.run_evolution({"Pb-206": 1.0}, 1e14, flux=1e14, energy_eV=30_000.0, mt_filter=[102])
print(run.final()["Bi-209"])
```
::::

::::{py:class} RunResult

Result of {py:meth}`NuclearService.run_evolution`. Used by the Results and Graph workspaces and stored in sessions.

```{py:attribute} names
:type: list[str]
```

```{py:attribute} times
:type: list[float]

Saved times, s.
```

```{py:attribute} trajectories
:type: list[numpy.ndarray]

One inventory vector per saved time.
```

```{py:attribute} heat
:type: list[float]

Heat release at each saved time, MeV s⁻¹ per unit of initial inventory.
```

```{py:attribute} isotopes
:type: list[~core.entities.Isotope]
```

```{py:attribute} initial
:type: dict[str, float]
```

```{py:attribute} flux
:type: float
```

```{py:attribute} energy_eV
:type: float
```

```{py:attribute} t_end_s
:type: float
```

```{py:attribute} method
:type: str
```

```{py:attribute} targets
:type: list[str]

Target labels if the run used a reduced network; empty otherwise.
```

```{py:attribute} capture_sigma_barn
:type: numpy.ndarray | None

Snapshot of the (n,γ) cross sections used by the averaging.
```

```{py:method} final()

:returns: the inventory at the last saved time, by name.
:rtype: dict[str, float]
```
::::

::::{py:class} EqResult

Result of an equilibrium scan.

```{py:attribute} names
:type: list[str]
```

```{py:attribute} flux_list
:type: list[float]

Fluxes, n cm⁻² s⁻¹.
```

```{py:attribute} time_list
:type: list[float]

Irradiation time used for each flux, s.
```

```{py:attribute} N_eq
:type: list[numpy.ndarray]

Inventory for each flux.
```

```{py:attribute} Q_eq
:type: list[float]

Heat release for each flux, MeV s⁻¹ per unit of initial inventory.
```
::::

```{py:function} init_service(project_root, progress=None, **kwargs)

Create the shared service of the application if needed and initialise it; `kwargs` go to {py:meth}`NuclearService.init`.

:rtype: NuclearService
```

```{py:function} get_service()

:returns: the shared service instance (created on first call).
:rtype: NuclearService
```

```{py:function} is_initialized()

:returns: whether the shared service is initialised.
:rtype: bool
```
