# Isotope Chart: building the network

Here you decide which nuclides take part in the calculation, which data they use, and which reactions and decays connect them. The result is the **burnup matrix**.

```{image} ../_static/images/network.png
:alt: Isotope chart with a selected network
:class: screenshot
```

## Select nuclides

There are two ways, and they can be combined:

**Drag a rectangle** on the chart. The axes are proton number $Z$ and neutron number $N = A - Z$. Every nuclide in the rectangle is selected (up to 5000 candidates).

**Type labels** into the **Manual:** field, separated by spaces:

```text
Tl-206 Tl-207 Pb-206 Pb-207 Pb-208
```

Ranges within one element are allowed: `Tl206..Tl216`.

To leave a nuclide out, right-click its cell. Excluded nuclides are listed under the chart; **Un-exclude selected** and **Clear** bring them back.

## Set up the calculation

The configuration tabs on the right control what goes into the matrix.

### Calculation tab: reactor or astrophysics

| Mode | Cross sections | Typical energy |
|---|---|---|
| **Reactor physics** | pointwise σ(E) from ENDF-6, interpolated at the chosen neutron energy | 0.0253 eV (thermal), 1 MeV, 14.1 MeV (DT) |
| **Astrophysics** | Maxwellian-averaged cross sections (MACS) at the chosen $kT$ | 30 keV |

Pick the energy from the list or choose **Manual…** and type a value in eV. Each mode has its own list of data sources (multi-select). Their order decides which source wins when several contain the same quantity; see {doc}`../theory/cross-sections`.

### Neutron tab

Tick the reactions to include: **(n,γ)**, **(n,α)**, **(n,p)**, **(n,2n)**, **(n,f)**. For the *s*-process, (n,γ) alone is the usual choice.

### Decay tab

Choose the decay modes to include: β⁻, EC/β⁺, IT, α, neutron emission, spontaneous fission, proton emission. The checkboxes also control which arrows the chart draws.

## Build the matrix

Press **Build Burnup Matrix**. NuMatRx collects the data for every selected nuclide, links each decay and reaction to its daughter, and assembles the matrix. With **Show arrows** ticked, the chart draws every link.

Next, check the matrix in {doc}`results` before running a calculation.

## Find cycles

**Find Cycle Reactions** searches the network for closed paths — chains of reactions and decays that return to the starting nuclide, like

```text
Pb-206 →(n,γ)… Pb-209 →β⁻ Bi-209 →(n,γ) Bi-210 →β⁻ Po-210 →α Pb-206
```

The search has limits on time, cycle length and number of cycles so that it stays interactive on large networks; if a limit is reached, the status line says the list may be incomplete. A cycle shows that material *can* circulate; how much actually does depends on the rates — check this with an evolution run. Details: {doc}`../theory/cycles`.

## Network boundaries

A network is always a cut-out of the full nuclide chart. When a reaction produces a nuclide outside your selection, NuMatRx needs to know what to do with it:

- **open** channel — the material leaves the network (a sink);
- **closed** channel — this reaction is switched off for nuclides at the edge.

Decays are always kept. The open/closed choice is made per reaction type in **Results → Isotopes & Matrix → Open channels**. If the total inventory of a run decreases, material has left through an open boundary — expand the network if you need to follow it.
