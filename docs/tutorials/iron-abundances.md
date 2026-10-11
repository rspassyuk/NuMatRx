# Iron-seeded abundance calculation

**Goal:** build a broader network, average its trajectory over neutron exposure, and export an abundance distribution. This is a fixed-condition classical test, not a full stellar model.

## Define the network before calculating

Select a connected set beginning at Fe-56 and extending through the Pb–Bi region, including the desired terminal return channels such as Po-210 decay to Pb-206. A rectangle on the nuclide chart also includes off-path nuclides; it does not by itself specify a physically complete s-process network.

Record ground/metastable states, enabled branches, missing rates, source fallbacks, and channels leaving the network. Leave **Targets** empty when the aim is the full selected network rather than a source-to-target reduction. The isotope count is determined by your selection and data; **2638 is not a universal built-in network size**.

## Illustrative settings

| Setting | Value |
|---|---|
| Initial composition | Fe-56 = 1; all other entries zero |
| Thermal energy | MACS at 30 keV |
| Flux | $2.5\times10^{16}$ neutrons/cm²/s |
| Neutron channel | MT=102 |
| Decays | Available enabled decay channels; document any restrictions |
| Half-life preset | all |
| End time | $10^{15}$ s |
| Averaging | Exponential neutron exposure |
| Mean exposure | $\tau_0=0.3$ mbarn⁻¹ |

These parameters follow the broad application discussed with the software. They are insufficient to reproduce a numerical curve without the exact network, initial vector, nuclear data, boundary choices, solver revision, and saved grid.

## Calculate and average

1. Build and inspect the matrix and source diagnostics.
2. Run Evolution with the chosen solver. For adaptive CRAM-16 inspect any refinement failure; do not assume ordinary CRAM-16 or CRAM-48 is correct solely because it returns.
3. Check the total tracked inventory and minimum concentrations. Save the initial vector and trajectory.
4. Open **Trajectory averaging**, select **Exponential neutron exposure**, and enter `0.3`.
5. Click **Average results**. Check both the omitted tail and weight-integration error.
6. In Graph, choose **Abundance vs mass number A → Averaged results**.
7. Export both absolute $\overline N(A)$ and capture-weighted $\sum_i\sigma_i\overline N_i$ distributions. They have different units.

At this flux, $\tau_0=0.3$ corresponds to $t_0=1.2\times10^{10}$ s. It is a distribution scale, not the final integration time. Extend the integration range and refine the saved grid separately when assessing convergence.

## Comparing with Arlandini

The classical and stellar columns represent different physical models. Normalize each dataset to its own Sm-150 value if comparing shapes. Retain isotope membership for every mass bin, because a full network can include radioactive isobars absent from a reference table.

If Arlandini abundances are multiplied by NuMatRx cross sections, label them as reconstructed with common cross sections. They are not an independent prediction using Arlandini's native rates. Missing weights are gaps, not zeros. State any displayed limit such as $A\leq209$ and preserve the full numerical export.

The peak regions near A=88, 138, and 208 are useful landmarks, but visual resemblance is not a convergence test. Large ratios near the boundary require inspection of the constituent nuclides, capture and decay paths, and normalization. See [references](../references.md) and [methods](../methods.md).
