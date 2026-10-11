# Tutorial 2: The Pb–Bi–Po termination cycle

**You will learn** to build a network from evaluated data, find its cycles, follow the material flow to equilibrium, and find out which cross sections matter most.

## The physics

Slow neutron capture cannot build nuclei heavier than bismuth. Capture on Bi-209 produces Bi-210, which decays to Po-210, and Po-210 α-decays back to Pb-206. Matter that reaches the end of the *s*-process path is therefore sent back to lead and circulates:

```text
Pb-206 →(n,γ) Pb-207 →(n,γ) Pb-208 →(n,γ) Pb-209 →β⁻ Bi-209
                                                       │ (n,γ)
Pb-206 ←α Po-210 ←β⁻ Bi-210 ←──────────────────────────┘
```

This loop is the subject of the project's first publication (see {doc}`../reference/citing`).

## Build the network

::::{tab-set}

:::{tab-item} In the application
1. **Isotope Chart → Manual:**
   ```text
   Tl-206 Tl-207 Pb-206 Pb-207 Pb-208 Pb-209 Pb-210 Pb-211 Bi-209 Bi-210 Bi-211 Po-210 Po-211
   ```
2. **Calculation** tab: **Astrophysics**, energy **30 keV**.
3. **Neutron** tab: **(n,γ)** only. **Decay** tab: all modes.
4. Press **Build Burnup Matrix**, then check the links in **Results → Isotopes & Matrix**.
:::

:::{tab-item} In Python
This is what `examples/sprocess_termination.py` does:

```python
from core import IsotopeBuilder
from nuclear_data import EndfPathHolder, NuclearDataProvider

EndfPathHolder.init_xsdir("xsdir")
nd = NuclearDataProvider(
    dec_dir=EndfPathHolder.set_DEFAULT_DEC_DIR("ENDFB-VIII.0"),
    neu_dir=EndfPathHolder.set_DEFAULT_NEU_DIR("ENDFB-VIII.0"),
    macs_file=EndfPathHolder.set_DEFAULT_MACS_DIR("Endfb7"), macs_lib="Endfb7",
    endfb71_macs_dir=str(EndfPathHolder.get_ENDFB71_MACS_DIR()),
    eaf2010_macs_dir=str(EndfPathHolder.get_EAF2010_MACS_DIR()),
    talys_dir=str(EndfPathHolder.get_TALYS_DIR()),
)
specs = [(81, "Tl", 206), (81, "Tl", 207),
         (82, "Pb", 206), (82, "Pb", 207), (82, "Pb", 208),
         (82, "Pb", 209), (82, "Pb", 210), (82, "Pb", 211),
         (83, "Bi", 209), (83, "Bi", 210), (83, "Bi", 211),
         (84, "Po", 210), (84, "Po", 211)]
isotopes = IsotopeBuilder(nd).build_range(
    specs, E_eV=30_000.0, mt_filter=[102], prefer_macs=True)
```
:::
::::

With ENDF/B-VIII.0 decay data and the default MACS priority, the links look like this (cross sections are MACS at 30 keV; the source is in brackets):

```text
Pb-206  stable      (n,γ)→Pb-207  0.0136 b  [rawmacs]
Pb-207  stable      (n,γ)→Pb-208  0.00827 b [rawmacs]
Pb-208  stable      (n,γ)→Pb-209  0.000656 b [rawmacs]
Pb-209  T½=3.25 h   β⁻→Bi-209;  (n,γ)→Pb-210  0.00361 b [eaf2010]
Bi-209  T½≈2e19 y   α→out;      (n,γ)→Bi-210  0.00335 b [rawmacs]
Bi-210  T½=5.01 d   β⁻→Po-210;  α→Tl-206 (1.3e-6); (n,γ)→Bi-211 [eaf2010]
Po-210  T½=138 d    α→Pb-206;   (n,γ)→Po-211 [eaf2010]
…
```

Note how the data come from different libraries: NuMatRx takes each value from the first source in the priority list that has it ({doc}`../theory/cross-sections`).

## Find the cycles

Press **Find Cycle Reactions** in the chart, or in Python:

```python
from core import CycleAnalyzer

cycles = CycleAnalyzer(isotopes).find_all_cycles(max_length=10)
for c in cycles:
    print(" → ".join(c.isotope_names), f"({c.n_reactions} captures, {c.n_decays} decays)")
```

The search finds 14 elementary cycles in this network. The classical one is

```text
Pb-206 → Pb-207 → Pb-208 → Pb-209 → Bi-209 → Bi-210 → Po-210   (4 captures, 3 decays)
```

The others are variants through Pb-210, Tl-206/207 and Po-211. A cycle shows a possible path; the evolution run shows how much material actually takes it.

## Follow the material flow

Start from pure Pb-206 at $\Phi = 10^{14}$ n/cm²/s and run up to $10^{14}$ s (Results → Evolution, or in Python):

```python
import numpy as np
from core import BurnupConfig, BurnupMatrix

cfg = BurnupConfig(flux=1e14)
cfg.enable_specific_reactions([102])
cfg.set_decay_time_filter("all")
matrix = BurnupMatrix(isotopes, cfg)
matrix.build()

names = matrix.names()
N0 = np.zeros(len(names)); N0[names.index("Pb-206")] = 1.0
times, traj = matrix.evolve(N0, [0.0] + list(np.logspace(8, 14, 120)))
```

For the eight main nuclides you get (rounded):

| $t$ [s] | Pb-206 | Pb-207 | Pb-208 | Bi-209 | Po-210 |
|---|---|---|---|---|---|
| $10^{10}$ | 0.987 | 0.013 | 6e-5 | 1e-8 | 7e-14 |
| $10^{11}$ | 0.873 | 0.122 | 0.005 | 1e-5 | 7e-11 |
| $10^{12}$ | 0.257 | 0.461 | 0.275 | 0.0066 | 4e-8 |
| $10^{13}$ | 0.035 | 0.055 | 0.766 | 0.144 | 8e-7 |
| $10^{14}$ | 0.037 | 0.060 | 0.755 | 0.148 | 9e-7 |

After about $10^{13}$ s the composition stops changing: the cycle has reached equilibrium, with three quarters of the material in Pb-208 — the nuclide with the smallest capture cross section, where the flow is slowest.

The time to reach equilibrium scales as $1/\Phi$: at $\Phi = 10^{16}$ n/cm²/s the same composition is reached after about $10^{11}$ s.

## Equilibrium for many fluxes

**Results → Equilibrium**, mode **Auto plateau**, fluxes `1e12 1e13 1e14 1e15 1e16`, then **Calculate Equilibrium**. For each flux NuMatRx finds the plateau and reports its time and heat. In Python:

```python
N_eq, t_eq = matrix.solve_equilibrium(N0)
print(f"plateau reached at t = {t_eq:.2e} s")
```

Compare the plateaus in **Graph → Equilibrium N_eq vs flux**. The long-lived members of the cycle (Pb-206 to Bi-209) reach the same equilibrium fractions at every flux — only the time to get there changes, as $1/\Phi$. The short-lived ones grow with the flux: Po-210 is about $9\times10^{-7}$ at $10^{14}$ n/cm²/s but $9\times10^{-5}$ at $10^{16}$ n/cm²/s, because its abundance is set by the balance between production by capture and destruction by decay.

## Which cross sections matter?

**Results → Sensitivity**: target **Bi-209** concentration at the **plateau**, type **σ cross-section**, δ = 1 %, two-sided. Press **Run Sensitivity**. The ranked list shows how much a 1 % change of each capture cross section changes the equilibrium Bi-209 abundance:

| Parameter | $S$ |
|---|---|
| Bi-209 (n,γ) | −0.852 |
| Pb-208 (n,γ) | +0.755 |
| Pb-207 (n,γ) | +0.060 |
| Pb-206 (n,γ) | +0.036 |

The numbers have a simple meaning. In a cycle at equilibrium the flow $\sigma_i N_i \Phi$ is the same through every member, so each abundance is proportional to $1/\sigma_i$. Normalised to the total, this gives

$$
S_{\mathrm{Bi}}(\sigma_k) = X_k \quad (k \neq \mathrm{Bi}), \qquad
S_{\mathrm{Bi}}(\sigma_{\mathrm{Bi}}) = -(1 - X_{\mathrm{Bi}}),
$$

where $X_k$ is the equilibrium fraction of nuclide $k$: $X_{\mathrm{Pb208}} = 0.755$ and $1 - X_{\mathrm{Bi}} = 0.852$, exactly as in the table. The Bi-209 abundance is controlled by its own cross section and by that of Pb-208, the bottleneck of the cycle.

## Open or closed boundaries?

Some captures lead out of the network: on Po-210 in the eight-nuclide network of {doc}`../getting-started/first-gui-run`, on Pb-211, Bi-211 or Po-211 in the thirteen-nuclide network here. With **closed** channels (the default) these reactions are switched off; with **open** channels (Results → Isotopes & Matrix → Open channels) the material leaves the network.

How much it matters depends on the network. In the thirteen-nuclide network, the boundary nuclides are so short-lived or so little populated that the total inventory stays 1.0000 either way. In the eight-nuclide network, captures on Po-210 leave the network: at $\Phi = 10^{16}$ n/cm²/s about 7 % of the material is gone after $10^{13}$ s and half after $10^{14}$ s. If the total inventory of your run decreases, look at the open channels first, and add the missing daughters to the network if you need to follow them.
