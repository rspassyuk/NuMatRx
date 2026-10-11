# Trajectory averaging

First calculate Evolution or open a saved result. Choose one distribution:

| Selection | Inputs | Meaning |
|---|---|---|
| Time average over interval | Start time and End time, seconds | Uniform temporal mean over the selected interval |
| Exponential irradiation durations | Mean duration t0, seconds | Mixture of irradiation endpoints weighted by an exponential duration distribution |
| Exponential neutron exposure | Mean exposure tau0, mbarn⁻¹ | Equivalent exposure-distribution model for constant positive flux |

For the uniform mode, an empty End time uses the final saved time. The interval must satisfy 0 ≤ start < end ≤ final time. For the exponential time mode, integration runs from zero to the trajectory endpoint; t0 does not set that endpoint.

Click **Average results**. Inspect **Isotopes**, **Mass numbers** and the diagnostics. **Mean N(A)** sums the averaged inventories of equal-A isotopes. **Mean fraction(A)** divides that sum by the total averaged inventory. **Sum sigma_i N_i** sums isotope-wise weighted values, in barn times input inventory.

The exponential modes do not renormalize the uncovered tail. A high coverage does not guarantee adequate temporal resolution; inspect the weight error and compare finer/longer trajectories. Significant negative input concentrations block averaging. See the formulas and normalization in [Methods](../methods.md).

Use **Export averaged results** for CSV/TXT with parameters and both tables. **Save averaged session** stores the run and its latest average. To plot it, select Graph → Abundance vs mass number A → **Averaged results**. Repeating averaging replaces the attached average; save separate sessions for parameter comparisons.

## Solver independence

Averaging accepts a saved trajectory; it is not restricted to adaptive CRAM-16. Ordinary CRAM-16, CRAM-48, and Padé results can be averaged when they pass the input checks. A negative-inventory error refers to the trajectory values, not a ban on the method name. Saved sessions retain their old values after a source-code update.

## Numerical diagnostics

- **Coverage / tail:** how much of the chosen exponential distribution is included.
- **Weight integral / relative error:** whether the saved grid resolves the weighting function.
- **Inventory range:** loss or gain within the tracked network, which needs physical and boundary interpretation.
- **Minimum N / negatives:** signed values and possible numerical problems; log plots cannot show negative entries.
- **Cross-section availability:** whether capture-weighted outputs can be formed.

Fine internal solver steps and a fine saved grid address different errors. Refine the output grid through the Python API and extend the interval separately. Do not loosen diagnostic thresholds solely to remove an inconvenient discrepancy.
