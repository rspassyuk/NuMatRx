# Overview of the application

The main window has four workspaces, switched from the toolbar on the left. They follow the order of a calculation:

```{list-table}
:header-rows: 1
:widths: 18 42 40

* - Workspace
  - What you do there
  - Result
* - {doc}`Periodic Table <periodic-table>`
  - Browse decay and neutron data for any isotope and compare libraries.
  - You know which data are available.
* - {doc}`Isotope Chart <isotope-chart>`
  - Select nuclides, choose reactor or astrophysics mode, data sources and channels.
  - The burnup matrix of your network.
* - {doc}`Results <results>`
  - Set the initial composition and irradiation, then calculate evolution, equilibrium or sensitivity; average a trajectory.
  - Inventories, heat, coefficients — as tables.
* - {doc}`Graph <graphs>`
  - Plot any of these results; switch units and normalisation.
  - Figures ready for export.
```

## How the pieces connect

```text
 Periodic Table          Isotope Chart                Results                    Graph
 ──────────────          ─────────────                ───────                    ─────
 inspect data   ──▶   select nuclides       ──▶   Evolution            ──▶   concentrations
                      mode + energy               Equilibrium                 heat
                      data sources                Sensitivity                 abundances
                      channels                    Trajectory averaging        sensitivity
                      Build Burnup Matrix
```

Everything goes through one calculation service in the background, so the table in *Results* and the curve in *Graph* always show the same run. Changing a plot setting never recalculates anything; changing the flux, the nuclides or the data does — press the calculation button again.

## General tips

- Numeric fields accept scientific notation: `1e14`, `2.5e16`.
- **View → Theme** switches between light and dark; **View → Panels** brings back a closed panel.
- The application keeps the latest result of each calculation type. Save a session before you start a new run if you want to compare them (see {doc}`export-sessions`).
- The terminal window shows progress messages and errors in full — keep it visible.
