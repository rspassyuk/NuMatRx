# NuMatRx documentation

**Build a nuclear reaction network, calculate its evolution, and inspect the results.**

NuMatRx is a Python/PyQt5 application with a reusable numerical backend. It combines nuclear-data inspection, network construction, matrix-exponential solvers, and analysis of isotope inventories, heat, sensitivity, cycles, and averaged abundances.

## Choose a starting point

- **New user:** [install NuMatRx](installation.md), run the [data-free quick start](quickstart.md), then [connect nuclear data](nuclear-data.md).
- **Desktop user:** follow the [user guide](user-guide.md) from data selection to saved results.
- **Researcher:** use the [tutorials](tutorials/index.md), [methods](methods.md), and [reproducibility checklist](reproducibility.md).
- **Developer:** consult the [architecture](architecture.md) and [Python API guide](api.md).
- **A calculation failed:** start with [troubleshooting](troubleshooting.md).

The program calculates a user-selected network under fixed irradiation conditions. The Pb–Bi–Po tutorial demonstrates a compact network; the iron-seeded tutorial explains a broader abundance calculation. Neither example is a built-in stellar-evolution model.

```{toctree}
:maxdepth: 2
:caption: Getting started

installation
nuclear-data
quickstart
```

```{toctree}
:maxdepth: 2
:caption: Using NuMatRx

user-guide
tutorials/index
troubleshooting
```

```{toctree}
:maxdepth: 2
:caption: Scientific interpretation

methods
reproducibility
references
```

```{toctree}
:maxdepth: 2
:caption: Development

architecture
api
publication
changelog
```
