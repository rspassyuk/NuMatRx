# Tutorial 3: The *s*-process from iron to lead

**You will learn** to build a large network covering the whole *s*-process path, irradiate an iron seed, average the result over a distribution of neutron exposures, and compare it with the solar *s*-process abundances.

This is the classical *s*-process model: constant temperature and flux, an iron seed, and a mixture of exposures. It is a test of the network and the data, not a model of a star.

## The physics

Starting from Fe-56, each neutron capture adds one mass unit. When an unstable nuclide is reached, it usually β⁻-decays before the next capture, and the path moves to the next element. Step by step the material climbs along the valley of stability through the Sr–Y–Zr (A ≈ 88), Ba (A ≈ 138) and Pb (A ≈ 208) peaks, until it reaches the Pb–Bi–Po cycle of {doc}`termination-cycle`.

The classical analysis (Clayton and Ward 1974; Käppeler et al. 1989) describes the solar *s*-process abundances with an exponential distribution of neutron exposures $\tau = \int \Phi\,dt$, with a mean exposure $\tau_0 \approx 0.3$ mbarn⁻¹.

## 1. Build the network

In **Isotope Chart**, drag a rectangle from iron ($Z = 26$) to polonium ($Z = 84$) wide enough in $N$ to include the stable isotopes and the unstable nuclides one or two steps away from stability. In the calculation behind the published comparison the network contained about 2600 nuclides.

| Tab | Setting |
|---|---|
| Calculation | **Astrophysics**, energy **30 keV**; MACS sources in the order you want, e.g. user, rawmacs, ENDFB71, EAF2010, TALYS |
| Neutron | **(n,γ)** |
| Decay | all modes |

Press **Build Burnup Matrix**. Building takes a while for a network this size. Then check in **Results → Isotopes & Matrix**:

- every stable nuclide on the path has a capture cross section;
- the branching points you care about (for example Kr-85, Sm-151, Tm-170, W-185) have both a capture and a decay channel;
- Po-210 has its α decay to Pb-206, so that the termination cycle is closed.

## 2. Irradiate

In **Results → Evolution**:

| Control | Value |
|---|---|
| Initial conditions | Fe-56 = 1, all others 0 |
| Flux Φ | `2.5e16` n/cm²/s |
| Time end | `1e15` s |
| Method | CRAM-16 (adaptive) |
| Target isotopes | empty — follow the whole network |

Press **Calculate Evolution**. Move the **Time step** slider and watch the material move from iron to the heavy elements. The *mass numbers* part of the table shows the sum for each $A$.

```{tip}
The adaptive solver controls its own internal steps and is the safest choice for large, stiff networks. Compare with CRAM-48 on a few times if you want an independent check.
```

## 3. Average over neutron exposures

A single irradiation is not what we see in the Sun: the solar material is a mixture of matter that was exposed to different neutron doses. In the **Trajectory averaging** panel:

1. Choose **Exponential neutron exposure**.
2. Enter $\tau_0 = 0.3$ mbarn⁻¹.
3. Press **Average results**.

At this flux, $\tau_0 = 0.3$ mbarn⁻¹ corresponds to a mean duration $t_0 = 1.2\times10^{10}$ s, well inside the calculated range of $10^{15}$ s, so the coverage is essentially complete. Check the diagnostics anyway: coverage, weight-integral error and inventory range.

## 4. Plot the abundance distribution

In **Graph**, choose **Abundance vs mass number A**, source **Averaged results**:

- **Absolute** shows $\overline N(A)$, the mean inventory at each mass number per initial Fe-56 nucleus;
- **σN** shows $\sum_i \sigma_i \overline N_i$, the capture-weighted curve of the classical *s*-process analysis. In the classical picture it decreases smoothly, with steps at the magic neutron numbers $N = 50, 82, 126$.

**Export averaged results** saves both the isotope table and the mass-number table.

## 5. Compare with the solar *s*-process

Arlandini et al. (1999) tabulate *s*-process abundances from the classical model and from AGB-star models. To compare shapes:

1. sum the abundances of each data set by mass number;
2. divide each data set by its own value at Sm-150 (an *s*-only nuclide);
3. plot the ratio NuMatRx / reference against $A$.

The peaks at $A \approx 88$, 138 and 208 are the landmarks. Where the ratio leaves the 0.5–2 band, look at the nuclides contributing to that mass number: the network contains radioactive isobars that are not in the reference table, and differences in cross-section libraries show up directly.

## What to try next

- Change $\tau_0$ to 0.2 and 0.5 mbarn⁻¹ and watch the balance between the light and heavy peaks shift.
- Run **Sensitivity** with the Pb-208 or Bi-209 abundance as target to see which cross sections near the termination point matter most.
- Compare two MACS sources by rebuilding the matrix with a different priority, or use the **Library** option of the sensitivity analysis.
