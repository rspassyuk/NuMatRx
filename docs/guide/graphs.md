# Graph: plotting results

Choose a graph type, adjust the options and press **Plot / Refresh**. Plotting never reruns a calculation, so you can switch views freely.

```{figure} ../_static/images/plotting.png
:alt: Absolute isotope inventories plotted against time
:class: screenshot

Evolution concentration plot in Absolute mode, with isotope filters and display controls.
```

## Graph types

| Graph type | Shows | Options |
|---|---|---|
| **Concentrations vs time** | inventory of each nuclide during the evolution | nuclide filter; Absolute / Relative / σ·N |
| **Heat release vs time** | total heat release | MeV/s or W/cm³ |
| **Abundance vs mass number A** | sums over each mass number | source: **Time slice** or **Averaged results**; Absolute / Relative / σN |
| **Equilibrium heat vs flux** | heat at the evaluation time for each flux of a scan | MeV/s or W/cm³ |
| **Equilibrium N_eq vs flux** | inventories at the scan evaluation times versus flux | N/N_tot / Absolute / σ·N |
| **Sensitivity Analysis** | ranked sensitivity coefficients with their signs | — |


## Flux and sensitivity views

::::{tab-set}

:::{tab-item} Inventories vs flux
```{figure} ../_static/images/graphs_equilibrium.png
:alt: Relative inventories from a neutron-flux scan
:class: screenshot

Relative inventories versus neutron flux. The plotted inventories come from the saved Equilibrium scan, which can use automatic plateau searches or manually specified times.
```
:::

:::{tab-item} Heat vs flux
```{figure} ../_static/images/graphs_heat.png
:alt: Channel-energy release versus neutron flux in MeV per second per nucleus
:class: screenshot

The selected display is MeV/s per nucleus. The W/cm³ control selects the density-based conversion; the screenshot does not show that mode.
```
:::

:::{tab-item} Sensitivity
```{figure} ../_static/images/graphs_sensitivity.png
:alt: Signed sensitivity coefficients for Pb-209 at 1e10 seconds
:class: screenshot

Sensitivity of the Pb-209 inventory at 10¹⁰ s. Positive and negative bars show the direction of the response to the selected perturbations.
```
:::

::::

For mass-number abundance screenshots and averaging modes, see {doc}`averaging`.

## Useful details

- **Time slice**: the abundance plot follows the *Time step* slider of the Evolution tab.
- **Averaged results**: the plot shows the latest trajectory average; change the average in the averaging panel, not with the slider.
- **W/cm³** needs the material density; the conversion is explained in {doc}`../theory/heat-and-sensitivity`.
- Logarithmic axes cannot show zero or negative values; such points are simply not drawn.
- The plot follows the application theme (**View → Theme**).

## Export a figure

Use the Matplotlib toolbar under the plot to zoom, pan and **save** the figure (PNG, PDF, SVG). For a publication, export the numbers as well (see {doc}`export-sessions`) and state the units, the normalisation and the averaging in the caption.
