# Solvers

All solvers compute the same quantity, $\mathbf N(t) = e^{\mathbf A t}\mathbf N(0)$ for a constant matrix. They differ in how they approximate the exponential.

| Solver | GUI name | Code name | Best for |
|---|---|---|---|
| CRAM-16 | CRAM-16 | `cram16` | everyday use; fast and accurate for burnup matrices |
| Adaptive CRAM-16 | CRAM-16 (adaptive) | `cram16_adaptive` | large, stiff networks and long times; checks its own error |
| CRAM-48 | CRAM-48 | `cram48` | an independent high-order cross-check |
| Padé | Padé (expm) | `pade` | small networks; a reference from SciPy |
| Taylor series, BDF | — | `taylor`, `bdf` | Python API only, for experiments |

## Why matrix exponentials?

Burnup matrices are **stiff**: decay constants span from $10^{-20}$ s⁻¹ (nearly stable nuclides) to $10^{6}$ s⁻¹ (very short-lived ones). Step-by-step ODE integrators must take tiny steps to stay stable. Evaluating the matrix exponential directly avoids the problem: a single, stable "step" can cover any time interval.

## CRAM

The Chebyshev Rational Approximation Method (Pusa & Leppänen 2010) replaces $e^{z}$ on the negative real axis — where the eigenvalues of a burnup matrix lie — by the best rational approximation of order 16. In partial-fraction form,

$$
\mathbf N(t) \approx \alpha_0\,\mathbf N(0) + 2\,\mathrm{Re}\sum_{j=1}^{8} \alpha_j\,\mathbf x_j,
\qquad (\mathbf A t - \theta_j \mathbf I)\,\mathbf x_j = \mathbf N(0),
$$

with tabulated poles $\theta_j$ and residues $\alpha_j$. Each term is one sparse linear solve, so the method scales to thousands of nuclides; no dense exponential is formed.

**CRAM-16** applies this once from $t = 0$ to each output time.

**Adaptive CRAM-16** splits the interval into internal steps and controls their size by step doubling: each step is computed once with step $h$ and once as two half steps, and accepted only if

- the two results agree within a relative tolerance $10^{-9}$ and an absolute tolerance of $10^{-14}$ times the initial total inventory;
- no inventory becomes significantly negative;
- the total inventory is conserved (closed networks) or does not grow (networks with losses).

If a step fails, it is halved; if it passes easily, the next one is doubled. Negative values are never clipped and results are never renormalised — a calculation that cannot meet the checks stops with an error instead of returning a doubtful answer.

**CRAM-48** uses order 48 in the incomplete partial factorisation form (Pusa 2016), with 24 poles applied one after another. It is a separate implementation, which makes it a good independent check on CRAM-16.

## Padé

SciPy's `expm` (scaling and squaring with a Padé approximant; Virtanen et al. 2020) forms the full dense matrix exponential and multiplies it by $\mathbf N(0)$. It is very accurate for small and moderate networks and is used as a reference in the tests. For thousands of nuclides it becomes slow and memory-hungry.

## Choosing a solver

- Start with **CRAM-16**.
- For a network of thousands of nuclides, or when you integrate over very long times, use **CRAM-16 (adaptive)**.
- To make sure a result is not a numerical artefact, repeat it with a second solver (CRAM-48 or, for small networks, Padé). On the test chains of {doc}`../tutorials/decay-chain` all four agree to $10^{-14}$.

## Verification

The repository tests (`tests/test_cram*.py`, `tests/test_all.py`) compare the solvers with analytical solutions for closed, open and stiff decay chains, check inventory conservation and the absence of negative values. Run them with

```bash
python -m unittest discover -s tests -p "test_*.py"
```

These tests verify the numerics. Whether the result describes nature depends, in addition, on the network and the nuclear data you choose.
