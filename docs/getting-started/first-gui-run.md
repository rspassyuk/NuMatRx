# Your first run in the application

In ten minutes you will build a small network in the lead–bismuth region, irradiate it with neutrons and plot the result. You need the nuclear data from {doc}`nuclear-data`.

## 1. Look at the data

Start the application. In **Periodic Table**, click **Pb**, then **Pb-209**. The panels show its half-life (about 3.25 h), its β⁻ decay to Bi-209 and its neutron reactions.

```{image} ../_static/images/registry.png
:alt: Periodic Table workspace with Pb-209 selected
:class: screenshot
```

## 2. Build the network

Open **Isotope Chart** and type the nuclides into the **Manual:** field:

```text
Pb-206 Pb-207 Pb-208 Pb-209 Pb-210 Bi-209 Bi-210 Po-210
```

Then set up the calculation in the tabs on the right:

- **Calculation** tab: choose **Astrophysics** and the energy **30 keV**.
- **Neutron** tab: tick **(n,γ)**.
- **Decay** tab: keep all decay modes enabled.

Press **Build Burnup Matrix**. Arrows on the chart now show every connection: neutron captures, β⁻ decays and the α decay of Po-210 back to Pb-206.

```{image} ../_static/images/network.png
:alt: Isotope chart with the selected nuclides and their links
:class: screenshot
```

## 3. Run the evolution

Go to **Results → Evolution**.

| Control | Value |
|---|---|
| Initial conditions | press **⟳ Load matrix isotopes**, then set Pb-206 = 1 and leave the rest at 0 |
| Flux Φ [n/cm²/s] | `1e14` |
| Time end | `1e14` s |
| Method | CRAM-16 |

Press **Calculate Evolution**. The table fills with the inventory of every nuclide; drag the **Time step** slider to move through time.

```{image} ../_static/images/evolution.png
:alt: Evolution results table
:class: screenshot
```

## 4. Plot it

Open **Graph**, choose **Concentrations vs time** and press **Plot / Refresh**. You can follow the material along the chain:

- up to about $10^{11}$ s, Pb-206 is slowly converted into Pb-207 and Pb-208;
- around $10^{12}$ s Bi-209 appears, fed by the β⁻ decay of Pb-209;
- after about $10^{13}$ s the curves become flat. Material now circulates around the Pb–Bi–Po cycle, and the composition no longer changes: roughly three quarters Pb-208, 15 % Bi-209, the rest Pb-206 and Pb-207, with traces of Po-210.

```{image} ../_static/images/plotting.png
:alt: Concentrations of the selected nuclides versus time
:class: screenshot
```

## 5. Keep the result

- The **csv** and **txt** export buttons write the numbers of the run.
- **Save…** stores the run in a `.kaz` session file; **Open…** shows a saved session in a separate window.

## Where next

- The {doc}`../guide/overview` explains every workspace in detail.
- {doc}`../tutorials/termination-cycle` continues with this network: cycles, equilibrium and sensitivity.
- {doc}`../tutorials/s-process-from-iron` builds a full network from Fe-56 to the termination region.
