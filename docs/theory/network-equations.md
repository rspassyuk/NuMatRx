# Network equations

## The Bateman equations in matrix form

Let $N_i(t)$ be the amount of nuclide $i$. It is produced by decays and reactions of other nuclides $j$ and destroyed by its own decays and reactions:

$$
\frac{dN_i}{dt} =
\sum_{j \neq i} \left( \lambda_j\, b_{j\to i} + \Phi\, \sigma_{j\to i} \right) N_j
\;-\; \left( \lambda_i + \Phi \sum_r \sigma_{i,r} \right) N_i .
$$

Here $\lambda_j$ is the decay constant, $b_{j\to i}$ the branching fraction of the decay of $j$ into $i$, $\Phi$ the neutron flux and $\sigma$ the (effective) cross sections. For all nuclides together this is a linear system

$$
\frac{d\mathbf N}{dt} = \mathbf A\,\mathbf N ,
$$

and for constant conditions its solution is the matrix exponential

$$
\mathbf N(t) = e^{\mathbf A t}\,\mathbf N(0).
$$

## How NuMatRx assembles the matrix

Each column of $\mathbf A$ belongs to one parent nuclide:

| Entry | Contribution |
|---|---|
| diagonal $A_{ii}$ | $-\lambda_i - 10^{-24}\,\Phi \sum_r \sigma_{i,r}$ over all enabled channels |
| off-diagonal $A_{ij}$, decay | $+\lambda_j\, b_{j \to i}$ |
| off-diagonal $A_{ij}$, reaction | $+10^{-24}\,\Phi\, \sigma_{j \to i}$ |

The factor $10^{-24}$ converts barn to cm², with $\Phi$ in n/cm²/s. If a reaction can produce the daughter in the ground state or in an isomer, the effective cross section of each link already contains the isomeric yield, $\sigma_{j\to i} = \sigma_j \cdot Q_{j\to i}$.

Only **enabled** channels enter the matrix: those that pass the reaction (MT) filter, the decay-mode filter and the half-life preset, plus any manual decay channels. Disabling a channel is not the same as removing its nuclide — the nuclide stays in the network, it just loses that path.

## Units of $N$

$\mathbf N$ has the units of your initial composition. With Fe-56 = 1 every result is "per initial Fe-56 nucleus"; with nuclei/cm³ every result is in nuclei/cm³. The solver does not care, but the heat conversion to W/cm³ does (see {doc}`heat-and-sensitivity`).

## Flux or neutron density

Instead of a flux you can enter a neutron number density $n_n$. NuMatRx converts it with the speed of a neutron at the selected energy $E$:

$$
\Phi = n_n\, v, \qquad v = \sqrt{2E/m_n}.
$$

This is a single-energy conversion, consistent with a pointwise cross section at $E$. For MACS at a temperature $kT$, enter a flux directly if you want a specific thermal-average convention.

## Network boundaries

The network is always a finite piece of the nuclide chart. Transitions that lead outside it are handled as follows:

| Transition to a nuclide outside the network | Treatment |
|---|---|
| decay | always kept, as a loss (sink) |
| neutron reaction, channel **open** | kept, as a loss |
| neutron reaction, channel **closed** | switched off for this parent |

The setting is per reaction type (MT). With losses, the total $\sum_i N_i$ decreases; the decrease is exactly the material that left the network. In a closed network of decays and single-daughter reactions such as (n,γ), $\sum_i N_i$ is conserved — a useful check of a calculation.

## Time grid

An evolution run in the application saves the solution at 400 times: $t = 0$ and 399 times spaced logarithmically between *Time start* and *Time end*. Each saved point is computed directly from $\mathbf N(0)$, so errors do not accumulate from one output point to the next.
