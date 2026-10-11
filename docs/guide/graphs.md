# Graph: plotting results

Choose a graph type, adjust the options and press **Plot / Refresh**. Plotting never reruns a calculation, so you can switch views freely.

```{image} ../_static/images/plotting.png
:alt: Graph workspace with concentrations versus time
:class: screenshot
```

## Graph types

| Graph type | Shows | Options |
|---|---|---|
| **Concentrations vs time** | inventory of each nuclide during the evolution | nuclide filter; Absolute / Relative / σ·N |
| **Heat release vs time** | total heat release | MeV/s or W/cm³ |
| **Abundance vs mass number A** | sums over each mass number | source: **Time slice** or **Averaged results**; Absolute / Relative / σN |
| **Equilibrium heat vs flux** | heat at the plateau for each flux of an equilibrium scan | MeV/s or W/cm³ |
| **Equilibrium N_eq vs flux** | plateau inventories versus flux | N/N_tot / Absolute / σ·N |
| **Sensitivity Analysis** | ranked sensitivity coefficients with their signs | — |

## Useful details

- **Time slice**: the abundance plot follows the *Time step* slider of the Evolution tab.
- **Averaged results**: the plot shows the latest trajectory average; change the average in the averaging panel, not with the slider.
- **W/cm³** needs the material density; the conversion is explained in {doc}`../theory/heat-and-sensitivity`.
- Logarithmic axes cannot show zero or negative values; such points are simply not drawn.
- The plot follows the application theme (**View → Theme**).

## Export a figure

Use the Matplotlib toolbar under the plot to zoom, pan and **save** the figure (PNG, PDF, SVG). For a publication, export the numbers as well (see {doc}`export-sessions`) and state the units, the normalisation and the averaging in the caption.
