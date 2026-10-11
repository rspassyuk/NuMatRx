# Units and conventions

## Units

| Quantity | Unit in NuMatRx |
|---|---|
| time, half-life | s (the GUI time fields offer other units and convert) |
| decay constant | s⁻¹ |
| neutron flux $\Phi$ | n cm⁻² s⁻¹ |
| neutron density $n_n$ | n cm⁻³ |
| neutron energy (reactor mode) | eV |
| thermal energy $kT$ (astrophysics mode) | keV in the GUI and MACS tables; `E_eV` in eV in Python |
| cross section in links and matrices | barn ($10^{-24}$ cm²) |
| MACS in the user database | mb |
| channel energy `Q_MeV` | MeV |
| heat release | MeV/s per unit of initial inventory, or W/cm³ |
| neutron exposure $\tau$ | mbarn⁻¹ ($\tau = 10^{-27}\Phi t$) |
| inventory $N$ | the units of your initial composition |

```{tip}
30 keV is `30000` in an eV field and `30` in a keV field.
```

## Nuclide labels

| Where | Format | Example |
|---|---|---|
| GUI fields, `run_evolution`, `initial_by_label` | `Symbol-A`, isomer suffix `m1` | `Pb-206`, `Bi-210m1` |
| GUI manual field (also accepted) | `SymbolA`, ranges | `Pb206`, `Tl206..Tl216` |
| `user_db` keys | `Z-Symbol-A` | `82-Pb-206` |
| Python specs | `(Z, "Symbol", A)` | `(82, "Pb", 206)` |

## Reaction MT numbers

| MT | Reaction |
|---|---|
| 102 | (n,γ) radiative capture |
| 103 | (n,p) |
| 107 | (n,α) |
| 16 | (n,2n) |
| 18 | fission |

## Decay modes

| Name | Mode | ΔZ, ΔA |
|---|---|---|
| `beta-` | β⁻ | +1, 0 |
| `ec/beta+` | electron capture / β⁺ | −1, 0 |
| `it` | isomeric transition | 0, 0 |
| `alpha` | α | −2, −4 |
| `n` | neutron emission | 0, −1 |
| `p` | proton emission | −1, −1 |
| `sf` | spontaneous fission | — |

## Half-life presets

Keep only decays with a half-life up to:

| Preset | Upper limit |
|---|---|
| all | none |
| yearly | 3.156 × 10⁷ s |
| daily | 86 400 s |
| hourly | 3 600 s |
| minute | 60 s |
| second | 1 s |
