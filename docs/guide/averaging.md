# Trajectory averaging

An evolution run gives the inventory at each moment of one irradiation. Often you need something else: a **mean** over a period, or a **mixture** of material that was irradiated for different lengths of time. The classical *s*-process is the standard example — the solar abundances are reproduced by a mixture with an exponential distribution of neutron exposures. The *Trajectory averaging* panel does this for any saved evolution run.

```{figure} ../_static/images/results_averaging.png
:alt: Trajectory averaging table and diagnostics for an iron-seeded run
:class: screenshot

Exposure averaging with τ₀ = 0.3 mbarn⁻¹: isotope averages, integration diagnostics and export controls. This supplied screenshot retains the historical KazNRDC window title; the program is now named NuMatRx.
```

## Choose a distribution

| Distribution | Input | Meaning |
|---|---|---|
| **Time average over interval** | Start time, End time [s] | plain time average of one irradiation over the interval; empty End time = last saved time |
| **Exponential irradiation durations** | mean duration $t_0$ [s] | mixture of irradiations whose durations follow $e^{-t/t_0}$ |
| **Exponential neutron exposure** | mean exposure $\tau_0$ [mbarn⁻¹] | the same mixture expressed in neutron exposure $\tau = \Phi t$ — the classical *s*-process parameter |

For a constant flux, the last two are the same thing with $t_0 = \tau_0 / (10^{-27}\,\Phi)$. For example, $\tau_0 = 0.3$ mbarn⁻¹ at $\Phi = 2.5\times10^{16}$ n/cm²/s corresponds to $t_0 = 1.2\times10^{10}$ s. Formulas: {doc}`../theory/averaging`.

## Run it

1. Calculate an evolution (or open a saved session).
2. Choose the distribution and enter its parameter.
3. Press **Average results**.

Two tables appear: **Isotopes** with the mean inventory of every nuclide, and **Mass numbers** with the sums over each $A$:

| Column | Meaning |
|---|---|
| Mean N(A) | sum of the averaged inventories with this mass number |
| Mean fraction(A) | the same, divided by the total averaged inventory |
| Sum σᵢNᵢ | capture-weighted sum, in barn × inventory |

## Check the diagnostics

The diagnostics area reports the integration coverage, weights and inventory checks:

- **Coverage / tail** — how much of the exponential distribution lies inside the calculated time range. If the tail is large, calculate a longer evolution.
- **Weight integral / relative error** — whether the saved time grid resolves the weighting function.
- **Inventory range** — how much material left the network during the run.
- **Minimum N / negatives** — numerical noise in the trajectory.
- **Missing cross sections** — nuclides without a capture cross section; they appear as gaps in σN plots.

## Plot, export, save

- In **Graph**, choose **Abundance vs mass number A** and set the source to **Averaged results**.
- **Export averaged results** writes both tables with all parameters and diagnostics in the header.
- **Save averaged session** stores the run together with its average.

Averaging again with other parameters replaces the previous average. To compare several distributions, save a session for each.

## Averaged abundance views

Select **Abundance vs mass number A → Averaged results** in Graph. These screenshots show separate averaging modes; the time-step indicator does not set the averaging interval. The settings quoted below are those visible in the plot titles.

::::{tab-set}

:::{tab-item} Exposure: N
```{figure} ../_static/images/abundance_exposure_mean.png
:alt: Exposure-averaged mass-number abundances at tau0 0.3 inverse millibarn
:class: screenshot

Absolute mass-number abundances for τ₀ = 0.3 mbarn⁻¹. Each bin sums the averaged inventories of isotopes with the same mass number.
```
:::

:::{tab-item} Exposure: sigma N
```{figure} ../_static/images/abundance_exposure_capture_weighted.png
:alt: Capture-weighted exposure-averaged mass-number distribution
:class: screenshot

Capture-weighted mass-number sums for τ₀ = 0.3 mbarn⁻¹, displayed in barn × inventory. This is a different observable from the absolute abundance.
```
:::

:::{tab-item} Uniform time
```{figure} ../_static/images/abundance_uniform_time_mean.png
:alt: Uniform time-averaged abundances from 1e-6 to 1e12 seconds
:class: screenshot

Uniform time average over 10⁻⁶–10¹² s, shown in absolute inventory units.
```
:::

:::{tab-item} Exponential durations
```{figure} ../_static/images/abundance_exponential_duration_mean.png
:alt: Exponential duration average with mean 1.2e10 seconds and end 1e15 seconds
:class: screenshot

Exponential irradiation-duration mixture with t₀ = 1.2 × 10¹⁰ s and an end time of 10¹⁵ s, shown in absolute inventory units.
```
:::

::::
