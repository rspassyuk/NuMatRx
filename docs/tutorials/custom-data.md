# Tutorial 5: Adding your own nuclear data

**You will learn** to supply a half-life, a decay branch or a cross section that is missing from the libraries — or to replace a library value — without changing any code.

Your data go into the folder `user_db/` in the project. With the default priorities, user data are checked **first**, before ENDF and the MACS tables, so a value you enter takes precedence.

## The database file

Create `user_db/isotopes.json`. Each nuclide is a key of the form `Z-Symbol-A` (add `m1` for an isomer: `83-Bi-210m1`):

```json
{
  "82-Pb-209": {
    "decay": {
      "half_life_s": 11710.8,
      "channels": [
        {"mode": "beta-", "branch": 1.0, "Q_MeV": 0.644, "dz": 1, "da": 0, "rfs": 0}
      ]
    },
    "neutrons": {
      "102": {
        "Q_MeV": 5.12,
        "macs": [ {"kT_keV": 30, "sigma_mb": 1.5} ]
      }
    }
  }
}
```

| Field | Meaning | Unit |
|---|---|---|
| `half_life_s` | half-life | s |
| `mode` | decay mode, as in the ENDF reader: `beta-`, `ec/beta+`, `alpha`, `it`, `n`, `sf`, `p` | — |
| `branch` | branching fraction | fraction (0–1), not % |
| `Q_MeV` | energy released in the channel (used for heat) | MeV |
| `dz`, `da` | change of $Z$ and $A$ in the decay (β⁻: 1, 0; α: −2, −4) | — |
| `rfs` | final state of the daughter (0 = ground, 1 = first isomer) | — |
| `"102"` | the reaction, by its ENDF MT number | — |
| `kT_keV`, `sigma_mb` | a MACS point; give several temperatures to interpolate | keV, mb |

A full example with several Pb, Bi and Po nuclides is in `examples/user_db/spectra/isotopes.json`.

## Energy-dependent cross sections

For reactor mode, give a pointwise cross section as a CSV file `user_db/spectra/<key>_mt<MT>.csv`, for example `user_db/spectra/82-Pb-209_mt102.csv`:

```text
E_eV,sigma_barn
0.0253,0.65
1000,0.02
30000,0.0015
```

## Check that it is used

1. Restart the application. The terminal prints the user database entries it found:
   ```text
   [user_db] Loaded from: …/user_db/isotopes.json
   [user_db] 1 isotope(s) found: 82-Pb-209
   ```
2. Make sure **user** is ticked in the data-source lists of the **Isotope Chart** (it is by default).
3. After **Build Burnup Matrix**, the **Source** column of the isotope table in **Results → Isotopes & Matrix** shows where each value came from.

## Good practice

- Record where each value comes from (measurement, evaluation, your own estimate) — for example in a separate notes file next to `isotopes.json`.
- Give `Q_MeV` whenever you know it. Without it the channel still moves material but adds nothing to the heat.
- Keep the example database and your research database apart.
