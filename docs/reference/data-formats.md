# File formats

## `xsdir/` — nuclear libraries

```text
xsdir/
├── endf-6/<LIBRARY>/decay/      ENDF-6 decay files
├── endf-6/<LIBRARY>/neutrons/   ENDF-6 neutron files
├── MACS/rawmacs.txt
├── MACS/ENDFB71-EAF2010/ENDFB71/
├── MACS/ENDFB71-EAF2010/EAF2010/
└── TALYS/
    ├── recommended-ng-cross-sections/
    ├── recommended-na-cross-sections/
    ├── recommended-np-cross-sections/
    └── talys_macs_30_keV/
```

NuMatRx looks for `xsdir/` inside the project folder first, then next to it. See {doc}`../getting-started/nuclear-data`.

## `user_db/` — your own data

```text
user_db/
├── isotopes.json                 decay data and MACS points
└── spectra/<key>_mt<MT>.csv      pointwise cross sections
```

Keys have the form `Z-Symbol-A`, with `m1`, `m2` for isomers: `82-Pb-209`, `83-Bi-210m1`.

**`isotopes.json`**

```json
{
  "83-Bi-210": {
    "decay": {
      "half_life_s": 433000.0,
      "channels": [
        {"mode": "beta-", "branch": 0.99999, "Q_MeV": 1.16, "dz": 1,  "da": 0,  "rfs": 0},
        {"mode": "alpha", "branch": 1.0e-5,  "Q_MeV": 5.04, "dz": -2, "da": -4, "rfs": 0}
      ]
    },
    "neutrons": {
      "102": {"Q_MeV": 4.98, "macs": [{"kT_keV": 30, "sigma_mb": 2.0}]}
    }
  }
}
```

**`spectra/83-Bi-209_mt102.csv`**

```text
E_eV,sigma_barn
0.0253,0.0338
30000,0.0026
```

Field meanings and units are listed in {doc}`../tutorials/custom-data`.

## Initial conditions (CSV)

*Results → Evolution → load csv* reads two columns: nuclide label and initial amount.

```text
Fe-56,1.0
Ni-58,0.07
```

## Exports

**Evolution (`csv`/`txt`)** — one row per saved time: time, inventory of every nuclide, fractions and sums over mass number. Read the header line for the exact columns.

**Averaged results** — a first line starting with `#` holds a JSON object with all parameters, diagnostics and warnings; then two tables:

```text
# {"mode": "exposure", "tau0_mbarn_inv": 0.3, "exposure_coverage": 1.0, ...}
Isotope,A,Mean N,Mean fraction,Sigma N [barn * inventory]
Pb-206,206,0.2071,...
...

A,Mean N(A),Mean fraction(A),Sum sigma_i N_i [barn * inventory]
206,0.2071,...
```

Missing values are written as `NA`.

**Matrix (`BurnupMatrix.export_txt`)** — the matrix in text form, for inspection in other tools.

## Sessions (`.kaz`)

A Python pickle with the evolution result (`RunResult`), its trajectory average, the equilibrium result (`EqResult`) and the material density. Read it with `core.session.load_session`. Open only files from trusted sources.
