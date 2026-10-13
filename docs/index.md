# NuMatRx

{.hero-tagline}
**Build a nuclear reaction network from evaluated data, solve it with matrix-exponential methods, and see what happens to every isotope.**

NuMatRx is a Python desktop application and library for transmutation calculations. You pick nuclides on an isotope chart, NuMatRx collects their decay and neutron-reaction data from ENDF-6 libraries, MACS tables, TALYS or your own files, assembles the burnup matrix, and solves

$$
\frac{d\mathbf N}{dt} = \mathbf A\,\mathbf N
$$

with CRAM or Padé. The same engine serves reactor-physics problems (pointwise cross sections at a neutron energy) and stellar nucleosynthesis (Maxwellian-averaged cross sections at a temperature $kT$).

```{image} _static/images/network.png
:alt: Isotope chart with a selected Pb–Bi–Po network
:class: screenshot
```

## What you can calculate

::::{grid} 1 2 2 3
:gutter: 3

:::{grid-item-card} Decay chains
Inventories of any decay chain over time, with heat release from every channel.
:::

:::{grid-item-card} Neutron irradiation
Burnup under a constant neutron flux, with reaction rates at a chosen neutron energy.
:::

:::{grid-item-card} *s*-process nucleosynthesis
Slow neutron capture from an iron seed up to the Pb–Bi termination region at a stellar $kT$.
:::

:::{grid-item-card} Cyclic reactions
Closed reaction loops such as the Pb–Bi–Po termination cycle, found automatically on the network graph.
:::

:::{grid-item-card} Equilibrium and heat vs flux
Plateau inventories and equilibrium heat for a whole grid of neutron fluxes.
:::

:::{grid-item-card} Sensitivity
Which cross section, half-life or data library controls your result, ranked by sensitivity coefficient.
:::
::::

## Where to start

::::{grid} 1 2 2 2
:gutter: 3

:::{grid-item-card} {octicon}`download` Install
:link: getting-started/installation
:link-type: doc

Install from source on Windows, Linux or macOS, and connect the nuclear data.
:::

:::{grid-item-card} {octicon}`rocket` Quick start
:link: getting-started/first-gui-run
:link-type: doc

Build and solve a Pb–Bi–Po network through Python or the GUI.
:::

:::{grid-item-card} {octicon}`browser` Using the application
:link: guide/overview
:link-type: doc

A tour of the four workspaces: data, network, results and graphs.
:::

:::{grid-item-card} {octicon}`mortar-board` Tutorials
:link: tutorials/index
:link-type: doc

From a simple decay chain to the *s*-process from iron to lead.
:::

:::{grid-item-card} {octicon}`book` Theory
:link: theory/network-equations
:link-type: doc

The equations, solvers and averaging methods behind the numbers.
:::

:::{grid-item-card} {octicon}`code` Python API
:link: api/scripting
:link-type: doc

Run the same calculations from scripts and notebooks.
:::
::::

## The workflow in four steps

1. **Inspect data.** Look up half-lives, decay branches and cross sections in the *Periodic Table* workspace.
2. **Build the network.** Select nuclides on the *Isotope Chart*, choose reactor or astrophysics mode, and press *Build Burnup Matrix*.
3. **Calculate.** In *Results*, set the initial composition, flux and time, then run *Evolution*, *Equilibrium* or *Sensitivity*.
4. **Analyse.** Plot concentrations, heat and abundances in *Graph*, average over time or neutron exposure, export tables and save the session.

```{note}
The screenshots in this documentation show a compact Pb–Bi–Po network because it is small enough to read on screen. NuMatRx is not limited to this region: networks can start anywhere on the chart and contain thousands of nuclides. See the {doc}`tutorials/s-process-from-iron` tutorial for a network of about 2600 isotopes.
```

## Citing NuMatRx

If NuMatRx helps your research, please cite the project publications listed in {doc}`reference/citing`, together with the nuclear-data libraries you used.

```{toctree}
:hidden:
:caption: Getting started

getting-started/installation
getting-started/nuclear-data
getting-started/first-calculation
getting-started/first-gui-run
```

```{toctree}
:hidden:
:caption: Using the application

guide/overview
guide/periodic-table
guide/isotope-chart
guide/results
guide/averaging
guide/graphs
guide/export-sessions
```

```{toctree}
:hidden:
:caption: Tutorials

tutorials/index
tutorials/decay-chain
tutorials/termination-cycle
tutorials/s-process-from-iron
tutorials/heat-vs-flux
tutorials/custom-data
```

```{toctree}
:hidden:
:caption: Theory

theory/network-equations
theory/solvers
theory/cross-sections
theory/heat-and-sensitivity
theory/averaging
theory/cycles
```

```{toctree}
:hidden:
:caption: Python API

api/scripting
api/reference
```

```{toctree}
:hidden:
:caption: Reference

reference/data-formats
reference/units
reference/troubleshooting
reference/reproducibility
reference/architecture
reference/citing
```
