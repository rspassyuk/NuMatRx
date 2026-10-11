# API reference

Generated from the docstrings of the source code. For a guided introduction see {doc}`scripting`.

## Network objects — `core.entities`

```{eval-rst}
.. autoclass:: core.entities.Isotope
   :members: add_decay, add_reaction, getListOfDecays, getListOfReactions, name, from_symbol

.. autoclass:: core.entities.DecayLink

.. autoclass:: core.entities.ReactionLink
```

## Building networks from data — `core.registry`

```{eval-rst}
.. autoclass:: core.registry.IsotopeBuilder
   :members: build_isotope, build_range, missing_isotopes, print_report, link_products
```

## Burnup matrix and solvers — `core.burnup`

```{eval-rst}
.. autoclass:: core.burnup.BurnupConfig
   :members: set_open_boundary, set_open_boundary_mts, set_decay_mode_filter, enable_all_reactions, enable_specific_reactions, set_decay_time_filter, set_decay_time_range

.. autoclass:: core.burnup.BurnupMatrix
   :members: build, solve, evolve, heat_release, heat_curve, solve_equilibrium, find_plateau, equilibrium_heat, names, export_txt, export_evolution_txt, validate

.. autofunction:: core.burnup.equilibrium_heat_vs_flux
```

## CRAM — `core.cram`

```{eval-rst}
.. autofunction:: core.cram.cram16_step
.. autofunction:: core.cram.adaptive_cram16
.. autofunction:: core.cram.cram48_step
```

## Application service — `core.service`

```{eval-rst}
.. autoclass:: core.service.NuclearService
   :members: init, info, build_universe, build_universe_from_labels, build_matrix, run_evolution, run_equilibrium_scan, run_equilibrium_auto, run_sensitivity, minimal_subnetwork

.. autoclass:: core.service.RunResult
   :members: final

.. autoclass:: core.service.EqResult
```

## Averaging — `core.exposure`

```{eval-rst}
.. autoclass:: core.exposure.ExposureConfig
.. autoclass:: core.exposure.ExposureResult
.. autofunction:: core.exposure.average_run
.. autofunction:: core.exposure.average_exposure
.. autofunction:: core.exposure.isotope_values
.. autofunction:: core.exposure.mass_values
.. autofunction:: core.exposure.export_exposure
```

## Sensitivity — `core.sensitivity`

```{eval-rst}
.. autoclass:: core.sensitivity.SensitivityConfig
.. autoclass:: core.sensitivity.SensitivityEngine
   :members: run
.. autoclass:: core.sensitivity.SensitivityResult
   :members: ranked
.. autoclass:: core.sensitivity.SensRow
.. autoclass:: core.sensitivity.LibRow
```

## Cycles — `core.cycle_finder`

```{eval-rst}
.. autoclass:: core.cycle_finder.CycleAnalyzer
   :members: find_all_cycles, find_sccs, has_cycles, isotopes_in_cycles, cycles_through, print_report

.. autoclass:: core.cycle_finder.IsotopeCycle
   :members: length, isotope_names, is_pure_decay, is_pure_reaction, is_mixed, n_decays, n_reactions
```

## Sessions and plots — `core.session`, `core.plotting`

```{eval-rst}
.. autofunction:: core.session.save_session
.. autofunction:: core.session.load_session
.. autofunction:: core.plotting.plot_concentrations
.. autofunction:: core.plotting.plot_heat
.. autofunction:: core.plotting.plot_heat_vs_flux
```

## Nuclear data — `nuclear_data`

```{eval-rst}
.. autoclass:: nuclear_data.NuclearDataProvider
   :members: get_decay, get_macs, get_macs_with_source, get_sigma, get_sigma_with_source, get_reaction_data, set_dec_priority, set_macs_priority

.. autoclass:: nuclear_data.EndfPathHolder
   :members: init_xsdir

.. autoclass:: nuclear_data.UserDataReader
   :members: reload, list_isotopes
```
