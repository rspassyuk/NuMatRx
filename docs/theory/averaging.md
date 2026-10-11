# Time and exposure averaging

An evolution run gives $\mathbf N(t)$ for one irradiation. Averaging combines the saved trajectory with a weight function:

$$
\overline N_i = \int N_i(t)\, w(t)\, dt .
$$

The integral is evaluated with the trapezoidal rule on the saved time grid. The inventories themselves are never changed; only the weights differ between the modes.

## Uniform time average

$$
\langle N_i \rangle = \frac{1}{t_b - t_a}\int_{t_a}^{t_b} N_i(t)\,dt .
$$

Equal time intervals get equal weight. If $t_a$ or $t_b$ falls between saved points, NuMatRx inserts linearly interpolated end values. Note that this is not the plain mean of the table rows: the saved grid is logarithmic.

## Exponential distribution of irradiation durations

$$
w(t) = \frac{1}{t_0}\, e^{-t/t_0}, \qquad
\overline N_i = \int_0^{t_\mathrm{max}} N_i(t)\, w(t)\, dt .
$$

This describes a mixture: a fraction $w(t)\,dt$ of the material was irradiated for a time $t$ and then stopped. The part of the distribution that lies beyond the end of the run is

$$
1 - W = e^{-t_\mathrm{max}/t_0},
$$

and is reported as the *tail*. It is not renormalised; for $t_\mathrm{max} = 7\,t_0$ the tail is below 0.1 %.

## Exponential distribution of neutron exposures

The neutron exposure is the time-integrated flux. For a constant flux,

$$
\tau\,[\mathrm{mbarn^{-1}}] = 10^{-27}\,\Phi\, t ,
\qquad
\rho(\tau) = \frac{1}{\tau_0}\, e^{-\tau/\tau_0}.
$$

This is the classical *s*-process prescription (Clayton & Ward 1974; Käppeler et al. 1989): the solar main *s*-component is reproduced with $\tau_0 \approx 0.3$ mbarn⁻¹. For a constant flux the exposure and duration distributions are identical, with

$$
t_0 = \frac{\tau_0}{10^{-27}\,\Phi} .
$$

Exposure averaging needs a positive flux; time averaging also works for pure decay.

## Mass-number sums

After averaging, NuMatRx groups nuclides by mass number:

$$
\overline N(A) = \sum_{i:\,A_i = A} \overline N_i , \qquad
\overline f(A) = \frac{\overline N(A)}{\sum_i \overline N_i}, \qquad
S(A) = \sum_{i:\,A_i = A} \sigma_i\, \overline N_i .
$$

$S(A)$, the capture-weighted curve, uses each nuclide's own capture cross section (the MACS saved with the run), summed over isomeric branches. Nuclides without a cross section are left out of $S(A)$, which can produce gaps.

## Accuracy

Two diagnostics tell you whether an average can be trusted:

- the **tail** — how much of the distribution lies beyond the run; extend *Time end* to reduce it;
- the **weight-integral error** — the difference between the numerically integrated weight and its exact value; a large value means the saved grid is too coarse for $w(t)$.

Both are reported with every average and written to the export header.
