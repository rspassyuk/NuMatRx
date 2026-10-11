# Trajectory averaging

An evolution run gives the inventory at each moment of one irradiation. Often you need something else: a **mean** over a period, or a **mixture** of material that was irradiated for different lengths of time. The classical *s*-process is the standard example — the solar abundances are reproduced by a mixture with an exponential distribution of neutron exposures. The *Trajectory averaging* panel does this for any saved evolution run.

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

Under the tables, the panel reports how good the average is:

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
