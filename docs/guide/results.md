# Results: running calculations

The *Results* workspace holds everything that turns a matrix into numbers. Its tabs are **Isotopes & Matrix**, **Evolution**, **Equilibrium** and **Sensitivity**; the **Trajectory averaging** panel works on the latest evolution run (see {doc}`averaging`).

```{image} ../_static/images/evolution.png
:alt: Results workspace, Evolution tab
:class: screenshot
```

## Isotopes & Matrix

This tab lists every nuclide in the network with its half-life, enabled decay channels, cross sections and reaction rates.

**Check the network here before calculating.** Typical things to look for: a missing cross section, a decay branch you did not expect, a nuclide that should be in the network but is not.

| Control | What it does |
|---|---|
| **Add isotopes** / **Remove selected** | change the network without going back to the chart |
| **Open channels** | per reaction type: material leaving the network is a sink (open) or the reaction is disabled at the edge (closed) |
| **Decay library** + **Apply** | switch the decay data library |
| Reactions, Decays | the reaction types and decay modes that enter the matrix |
| Half-life preset | keep only decays with half-life up to: all, a year, a day, an hour, a minute, a second |
| **Manual decay channels** | add a decay by hand: parent, daughter, mode, half-life, branch |
| **Refresh Matrix View** | rebuild the matrix with the current settings |
| **Copy**, **Export CSV** | copy cells or save the isotope table |

Search the table with **Ctrl+F**.

### Manual decay channels

A manual channel overrides the library for that parent and mode and ignores the global decay filters. This lets you, for example, keep only β⁻ decays in a network but add the single α decay Po-210 → Pb-206 that closes the termination cycle. Leave the daughter empty to send the decay out of the network. Press **+ Add**, then **Refresh Matrix View**.

## Evolution

Evolution solves the network for a constant flux from time zero to the end time.

| Control | Meaning |
|---|---|
| Initial conditions | the starting inventory; **⟳ Load matrix isotopes** fills the table with all nuclides of the matrix, **load csv** reads a two-column file (label, value) |
| **Flux Φ** or **Neutron density n** | neutron flux in n/cm²/s, or density in n/cm³ converted to flux at the selected energy; `0` = decay only |
| Time start, Time end | the range of the saved time grid, with units |
| Method | CRAM-16, CRAM-16 (adaptive), CRAM-48, Padé (expm) — see {doc}`../theory/solvers` |
| Target isotopes | optional: restrict the run to the part of the network that leads to these nuclides — faster on large networks |

Press **Calculate Evolution**. The result is saved on a grid of 400 logarithmically spaced times. Use the **Time step** slider to move along it.

The table shows each nuclide and, below, the sums over each mass number $A$. The display modes are:

- **Absolute** — in the units of your initial inventory;
- **Relative** — divided by the total inventory at that time;
- **σN** — multiplied by the capture cross section.

The header shows the total heat release at the selected time.

```{tip}
Units follow your input. If you start with Fe-56 = 1, every number is "per initial Fe-56 nucleus". If you enter nuclei per cm³, you get nuclei per cm³.
```

## Equilibrium

Equilibrium runs the same network for a whole list of fluxes, each one as an independent irradiation from the initial composition.

- **Auto plateau** — for each flux, NuMatRx increases the time until the inventories stop changing.
- **Manual times** — you give one irradiation time per flux.

Enter fluxes separated by spaces (`1e12 1e13 1e14`) and press **Calculate Equilibrium**. The table lists flux, time reached and heat; the inventories are kept for the *Equilibrium* plots.

## Sensitivity

Sensitivity tells you which inputs control a chosen result. Choose:

1. **Target** — the inventory of one nuclide, or the total heat;
2. **When** — at a fixed time or at the plateau;
3. **What to vary** — **σ cross-section**, **λ half-life**, **Flux / Energy**, **Library**;
4. **Perturbation** δ (1 % by default) and whether to use **Two-sided (±δ central difference)**.

Press **Run Sensitivity**. Each parameter is changed on its own and the run repeated; the result is a list ranked by the size of the sensitivity coefficient $S$. The *Library* option instead repeats the run with each selected library and reports the spread. Theory: {doc}`../theory/heat-and-sensitivity`.

```{tip}
Every perturbation is a full calculation. Start with a small set of parameters on a large network.
```
