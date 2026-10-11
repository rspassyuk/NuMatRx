# Heat release and sensitivity

## Heat release

Every decay and reaction channel carries an energy $E$ (the `Q_MeV` of the link). The total energy release rate is

$$
H(t) = \sum_i N_i(t) \left[ \lambda_i \sum_d b_{id}\, E_{id} \;+\; 10^{-24}\,\Phi \sum_r \sigma_{ir}\, E_{ir} \right],
$$

summed over all enabled decay channels $d$ and reaction channels $r$ of every nuclide $i$, including those that lead out of the network. NuMatRx stores the bracket as one coefficient per nuclide, so $H$ at any time is a single dot product with $\mathbf N(t)$.

With $N$ per initial nucleus and $E$ in MeV, $H$ is in MeV/s per initial nucleus. The application converts it to a volumetric rate with the material density $\rho_m$ and the molar mass $M$ of the initial composition:

$$
Q\,[\mathrm{W/cm^3}] = H\,[\mathrm{MeV/s}] \times 1.602\times10^{-13}\,\frac{\mathrm J}{\mathrm{MeV}} \times \frac{\rho_m N_A}{M}.
$$

```{note}
$H$ is the energy released in the channels as given in the nuclear data. Where this energy is deposited — neutrinos escape, γ-rays may leave the material — is not modelled. A channel without an energy value moves material but adds nothing to $H$.
```

At an equilibrium plateau the composition no longer changes, but $H$ is not zero: the material keeps circulating, and every passage through a cycle releases energy.

## Equilibrium

For a given flux, NuMatRx looks for the time after which the composition stops changing:

- it starts from about ten times the slowest process time in the matrix,
- multiplies the time by 3 until the largest relative change of any inventory is below $10^{-4}$,
- and stops at $10^{25}$ s at the latest.

An *Equilibrium* scan in the application repeats this for each flux independently, always from the same initial composition.

When material can leave the network (open channels), there is no true steady state: the heat rises, passes a maximum and falls as material drains away. The Python function `equilibrium_heat_vs_flux` handles this case by taking the time of maximum heat as the plateau ({doc}`../tutorials/heat-vs-flux`). In the application, check the time reached for each flux and the total inventory before calling a result an equilibrium.

## Sensitivity coefficients

For a result $F$ (an inventory or the heat) and a parameter $p$ (a cross section, a decay constant, the flux or the energy), the dimensionless sensitivity is

$$
S_p = \frac{p}{F}\,\frac{\partial F}{\partial p}
\approx \frac{F\big(p(1+\delta)\big) - F\big(p(1-\delta)\big)}{2\,\delta\,F(p)},
$$

computed by changing one parameter at a time (OAT) and rebuilding the matrix (Koloczek et al. 2016). $\delta = 1\,\%$ by default. A one-sided difference is available when two-sided is switched off.

$S = 0.5$ means: a 1 % increase of $p$ increases $F$ by 0.5 %. The sign tells the direction. For a worked example with a simple interpretation see {doc}`../tutorials/termination-cycle`.

Two limits to keep in mind:

- OAT coefficients are **local**: they describe small changes around your input, one parameter at a time. Correlated or large uncertainties need a Monte Carlo study.
- If the baseline $F$ is zero, a relative coefficient is undefined.

The **Library** option does something different: it repeats the run with each selected library and reports the spread of the results, not a derivative.
