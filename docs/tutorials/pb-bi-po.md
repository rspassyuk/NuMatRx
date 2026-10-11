# Pb–Bi–Po network

**Goal:** use a small termination-region network to learn the GUI. This example is related to the project's published termination studies, but the settings below define a teaching run, not a reproduction of all published figures.

## Prerequisites

Install decay and capture data for the selected nuclides. Check that the sources contain the beta decays of Pb-209, Pb-210, and Bi-210 and the alpha decay of Po-210. Inspect metastable-state branches rather than merging them implicitly.

## Configure the run

1. Enter the following labels in the isotope chart's manual selection:

   ```text
   Pb206 Pb207 Pb208 Pb209 Pb210 Bi209 Bi210 Po210
   ```

2. Select the astrophysical/MACS route at **30 keV** (`30000` in an eV field).
3. Enable radiative capture, MT=102, and the required beta-minus and alpha decays. Choose half-life preset **all**.
4. Include the terminal return `Po-210 → Pb-206`. Inspect its rate and daughter link after building the matrix.
5. For this teaching example, choose open capture boundary channels and record this choice. Captures that leave the selected set can remove tracked material. Expand the network if you want those daughters explicitly.
6. Load matrix isotopes into Initial Conditions, set **Pb-206 = 1**, and set every other entry to zero.
7. Start with flux **1e14 neutrons/cm²/s**, final time **1e10 s**, and ordinary **CRAM-16**. Repeat with another solver to check numerical agreement on this small network.
8. In Graph, display selected concentrations versus time, then save the table and `.kaz` session.

## Inspect the result

The enabled path should contain captures towards Pb-209, beta decay towards Bi-209, capture towards Bi-210, beta decay towards Po-210, and alpha return to Pb-206 where the selected data supply these transitions. The cycle tool can help locate this path; it does not establish that the path dominates the material flow.

With open boundaries, the total tracked inventory may decrease. Plot the total and inspect outgoing channels instead of renormalizing away the loss. Missing or very weak links can change the result even if the same nuclide names are selected.

Equilibrium and sensitivity can now be explored with their own settings. A flux scan evaluates separate irradiations; it is not a time-dependent flux history. See [Results](../user-guide/results.md).
