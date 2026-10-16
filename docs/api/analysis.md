# Analysis: averaging, sensitivity and cycles

These tools work on a finished calculation or on a network. Theory: {doc}`../theory/averaging`, {doc}`../theory/heat-and-sensitivity`, {doc}`../theory/cycles`.

| Object | Purpose |
|---|---|
| {py:class}`~core.exposure.ExposureConfig`, {py:func}`~core.exposure.average_run` | average a trajectory over time or neutron exposure |
| {py:class}`~core.exposure.ExposureResult`, {py:func}`~core.exposure.mass_values` | averaged inventories and sums over mass number |
| {py:class}`~core.sensitivity.SensitivityConfig`, {py:class}`~core.sensitivity.SensitivityEngine` | one-at-a-time sensitivity coefficients |
| {py:class}`~core.cycle_finder.CycleAnalyzer` | closed reaction–decay cycles of a network |

## Time and exposure averaging — `core.exposure`

```{py:module} core.exposure
```

::::{py:class} ExposureConfig(tau0=0.3, tail_limit=1e-3, weight_rtol=5e-3, negative_atol=1e-14, negative_rtol=1e-10, mode="exposure", start_s=0.0, end_s=None, mean_time_s=1e9)

Settings of an average. The object is immutable (frozen dataclass).

```{py:attribute} mode
:type: str

`"exposure"` — exponential distribution of neutron exposures; `"time_exponential"` — exponential distribution of irradiation durations; `"time_uniform"` — plain time average over an interval.
```

```{py:attribute} tau0
:type: float

Mean neutron exposure for `mode="exposure"`, mbarn⁻¹.
```

```{py:attribute} mean_time_s
:type: float

Mean duration $t_0$ for `mode="time_exponential"`, s.
```

```{py:attribute} start_s
:type: float

Start of the interval for `mode="time_uniform"`, s.
```

```{py:attribute} end_s
:type: float | None

End of the interval for `mode="time_uniform"`, s; `None` uses the last saved time.
```

```{py:attribute} tail_limit
:type: float

A warning is given if the part of the distribution beyond the run is larger.
```

```{py:attribute} weight_rtol
:type: float

A warning is given if the numerical integral of the weight differs more than this from the exact value (grid too coarse).
```

```{py:attribute} negative_atol
:type: float

Absolute part of the tolerance for negative values in the trajectory.
```

```{py:attribute} negative_rtol
:type: float

Relative part of the same tolerance; larger negative values stop the averaging.
```
::::

::::{py:class} ExposureResult

Result of an average.

```{py:attribute} names
:type: list[str]
```

```{py:attribute} mean
:type: numpy.ndarray

Averaged inventory of each nuclide, in the units of the run.
```

```{py:attribute} sigma_barn
:type: numpy.ndarray

(n,γ) cross section of each nuclide used for σN values; `NaN` where unavailable.
```

```{py:attribute} coverage
:type: float

Fraction of the distribution inside the calculated time range (1 for a uniform average).
```

```{py:attribute} tail
:type: float

Fraction outside the range; it is not renormalised.
```

```{py:attribute} weight_integral
:type: float

Numerical integral of the weight function on the saved grid.
```

```{py:attribute} diagnostics
:type: dict

Initial, final, minimum and maximum total inventory, minimum value, number of negative values, weight error and nuclides without a cross section.
```

```{py:attribute} warnings
:type: list[str]

Human-readable warnings (long tail, coarse grid, inventory change, missing cross sections, …).
```

```{py:attribute} metadata
:type: dict

Provenance: flux, time range, mode, distribution and method.
```
::::

```{py:function} average_run(run, config, progress=None)

Average a {py:class}`~core.service.RunResult`. Only the run itself and its stored data are used, not the current settings of the application.

:rtype: ExposureResult
```

```{py:function} average_exposure(names, times, trajectories, flux, config, sigma_barn=None, metadata=None, progress=None)

The averaging itself: trapezoidal rule on the saved grid with the chosen weight. Small negative values are kept and reported.

:param times: strictly increasing times starting at 0, s.
:param trajectories: array of shape `(len(times), len(names))`.
:param flux: n cm⁻² s⁻¹; must be positive for `mode="exposure"`.
:param metadata: for `mode="exposure"` it must contain `constant_conditions=True`.
:raises ValueError: for invalid input, significant negative values or a non-positive average.
:rtype: ExposureResult
```

```{py:function} isotope_values(result, mode="absolute")

:param mode: `"absolute"`, `"relative"` (divided by the total) or `"sigma_n"` (multiplied by the cross section).
:returns: one value per nuclide.
:rtype: numpy.ndarray
```

```{py:function} mass_values(result, mode="absolute")

Sum {py:func}`isotope_values` over each mass number.

:returns: `(A, values)`.
:rtype: tuple[numpy.ndarray, numpy.ndarray]
```

```{py:function} export_exposure(result, path)

Write the isotope table and the mass-number table. The first line is `#` followed by a JSON object with all parameters, diagnostics and warnings. `.csv` uses commas, other extensions use tabs.
```

```{py:function} capture_snapshot(names, isotopes)

:returns: `(sigma, sources)` — summed (n,γ) cross section of each nuclide (barn, `NaN` if absent) and the data sources.
```

```{py:function} mass_number(name)

:returns: the mass number parsed from a label such as `"Bi-210m1"`.
:rtype: int
:raises ValueError: if the label cannot be parsed.
```

**Example**

```python
from core.exposure import ExposureConfig, average_run, mass_values, export_exposure

avg = average_run(run, ExposureConfig(mode="exposure", tau0=0.3))
print(avg.coverage, avg.warnings)
A, N_A = mass_values(avg, mode="sigma_n")
export_exposure(avg, "average.csv")
```

## Sensitivity — `core.sensitivity`

```{py:module} core.sensitivity
```

::::{py:class} SensitivityConfig

Settings of a sensitivity analysis (dataclass; all fields have defaults).

```{py:attribute} initial_by_label
:type: dict[str, float]

Initial inventory, e.g. `{"Pb-206": 1.0}`.
```

```{py:attribute} target_kind
:type: str

`"concentration"` (needs `target_label`) or `"heat"`.
```

```{py:attribute} target_label
:type: str | None

Nuclide whose inventory is the target.
```

```{py:attribute} eval_mode
:type: str

`"time"` — evaluate at `t_eval_s`; `"plateau"` — evaluate at equilibrium.
```

```{py:attribute} t_eval_s
:type: float

Evaluation time, s (default 10⁹).
```

```{py:attribute} types
:type: list[str]

What to vary: any of `"sigma"`, `"halflife"`, `"flux_energy"`, `"library"`.
```

```{py:attribute} delta
:type: float

Relative perturbation (default 0.01).
```

```{py:attribute} two_sided
:type: bool

Central difference with ±δ if `True`, one-sided otherwise.
```

```{py:attribute} scope_channels
:type: list[tuple[str, int]] | None

Limit the σ scan to `(isotope, MT)` pairs; `None` scans all channels.
```

```{py:attribute} scope_isotopes
:type: list[str] | None

Limit the half-life scan to these nuclides.
```

```{py:attribute} libraries
:type: list[str]

Libraries for the `"library"` type.
```

```{py:attribute} reference_library
:type: str | None

Reference for library deviations; `None` compares with the mean.
```

The run settings `flux`, `energy_eV`, `mt_filter`, `method`, `hl_preset`, `open_boundary_mts` and `prefer_macs` have the same meaning as in {py:meth}`NuclearService.run_evolution <core.service.NuclearService.run_evolution>`.
::::

::::{py:class} SensitivityEngine(service)

Runs the analysis on the working network of a {py:class}`~core.service.NuclearService`.

```{py:method} run(cfg, progress=None, should_cancel=None)

Compute the baseline, then change one parameter at a time, rebuild the matrix and solve again.

:type cfg: SensitivityConfig
:raises RuntimeError: if the service is not initialised.
:raises ValueError: if a concentration target has no `target_label`.
:rtype: SensitivityResult
```
::::

::::{py:class} SensitivityResult

```{py:attribute} target_desc
:type: str
```

```{py:attribute} base_value
:type: float

Value of the target without perturbation.
```

```{py:attribute} rows
:type: list[SensRow]

One row per perturbed parameter, sorted by |S|.
```

```{py:attribute} library_rows
:type: list[LibRow]
```

```{py:attribute} lib_stats
:type: dict[str, float]

Minimum, maximum, mean and standard deviation over libraries.
```

```{py:method} ranked()

:returns: rows sorted by |S| with `rank` filled in.
:rtype: list[SensRow]
```
::::

::::{py:class} SensRow

One coefficient: `parameter` (e.g. `"Bi-209 (n,γ)"`), `type` (`"σ"`, `"λ"`, `"Φ"`, …), `base`, `perturbed`, the coefficient `S` and its `rank`.
::::

::::{py:class} LibRow

One library: `library`, target inventory `N_i`, heat `Q` and `deviation_pct` from the reference.
::::

**Example**

```python
from core.sensitivity import SensitivityConfig, SensitivityEngine

cfg = SensitivityConfig(initial_by_label={"Pb-206": 1.0},
                        target_kind="concentration", target_label="Bi-209",
                        eval_mode="plateau", types=["sigma"],
                        flux=1e14, energy_eV=30_000.0, mt_filter=[102], prefer_macs=True)
result = SensitivityEngine(svc).run(cfg)
for row in result.rows[:3]:
    print(row.parameter, round(row.S, 3))
```

## Cycles — `core.cycle_finder`

```{py:module} core.cycle_finder
```

::::{py:class} CycleAnalyzer(isotopes)

Finds closed paths of decays and reactions in a linked network.

:param isotopes: isotopes with linked products, e.g. from {py:meth}`IsotopeBuilder.build_range <core.registry.IsotopeBuilder.build_range>`.

```{py:method} find_all_cycles(max_cycles=None, max_length=None, timeout_s=None, should_cancel=None, progress=None)

Enumerate elementary cycles by iterative depth-first search; each cycle is found once. After the call, the attribute `search_status` is non-empty if a limit or cancellation stopped the search early.

:param max_cycles: stop after this many cycles.
:param max_length: ignore longer cycles.
:param timeout_s: time limit, s.
:rtype: list[IsotopeCycle]
```

```{py:method} find_sccs()

Strongly connected components (Tarjan's algorithm), only groups with two or more nuclides or a self-loop.

:rtype: list[SCC]
```

```{py:method} has_cycles()

:rtype: bool
```

```{py:method} isotopes_in_cycles()

:rtype: list[~core.entities.Isotope]
```

```{py:method} cycles_through(isotope)

:returns: all cycles that contain this nuclide.
:rtype: list[IsotopeCycle]
```

```{py:method} print_report(cycles=None, max_show=30)

Print the components, a summary and the cycles.
```
::::

::::{py:class} IsotopeCycle

A closed path `steps[0] → … → steps[n-1] → steps[0]`.

```{py:attribute} steps
:type: list[CycleStep]
```

```{py:property} isotope_names
:type: list[str]
```

```{py:property} length
:type: int
```

```{py:property} n_decays
:type: int
```

```{py:property} n_reactions
:type: int
```

```{py:property} is_pure_decay
:type: bool
```

```{py:property} is_pure_reaction
:type: bool
```

```{py:property} is_mixed
:type: bool
```
::::

::::{py:class} CycleStep

One transition: `isotope`, readable `label`, `kind` (`"decay"` or `"reaction"`) and `mt` (for reactions).
::::

::::{py:class} SCC

A strongly connected component: `isotopes`, its `cycles` and the property `names`.
::::

**Example**

```python
from core import CycleAnalyzer

analyzer = CycleAnalyzer(isotopes)
cycles = analyzer.find_all_cycles(max_length=10, timeout_s=30)
for c in cycles:
    print(" → ".join(c.isotope_names), c.n_reactions, c.n_decays)
```
