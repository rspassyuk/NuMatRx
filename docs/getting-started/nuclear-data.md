# Nuclear data

NuMatRx does not ship with nuclear data. The libraries live in a folder called `xsdir`, which you download once and place next to the code.

## Download

The project provides a ready-made `xsdir` archive:

[Download datasets from Google Drive](https://drive.google.com/drive/folders/1Qvy23GtS8aMXxuuQK3cA7DE3uszLhbq4?usp=sharing)

You can also assemble `xsdir` yourself from the original distributions (NNDC, IAEA, JAEA). The folder layout below is what NuMatRx expects.

## Where to put it

Extract the archive so that `xsdir` sits **inside** the NuMatRx folder:

```text
NuMatRx/
├── core/
├── model/
├── nuclear_data/
├── user_db/          ← your own data (optional)
└── xsdir/
    ├── endf-6/
    ├── MACS/
    └── TALYS/
```

If there is no `xsdir` inside the project, NuMatRx also looks for one **next to** the project folder. This is handy if several checkouts share the same data:

```text
workspace/
├── NuMatRx/
└── xsdir/
```

```{warning}
Watch out for a doubled folder after extraction (`xsdir/xsdir/endf-6`). NuMatRx needs `endf-6` directly inside `xsdir`.
```

## What is inside

```text
xsdir/
├── endf-6/
│   └── ENDFB-VIII.0/          one folder per evaluated library
│       ├── decay/             decay sublibrary (half-lives, branches, energies)
│       └── neutrons/          neutron sublibrary (σ(E), isomeric branching)
├── MACS/
│   ├── rawmacs.txt            Maxwellian-averaged cross sections
│   └── ENDFB71-EAF2010/
│       ├── ENDFB71/           multi-temperature MACS from ENDF/B-VII.1
│       └── EAF2010/           multi-temperature MACS from EAF-2010
└── TALYS/
    ├── recommended-ng-cross-sections/
    ├── recommended-na-cross-sections/
    ├── recommended-np-cross-sections/
    └── talys_macs_30_keV/
```

`endf-6` and `MACS` are required; TALYS is optional. Other evaluated libraries (JEFF, JENDL, TENDL) go into `endf-6/` as additional folders with the same `decay/` and `neutrons/` structure. ENDF/B-VIII.0 is the default.

| Source | Provides | Used for |
|---|---|---|
| ENDF-6 libraries | half-lives, decay branches and energies; pointwise σ(E); isomeric branching | decay data; reactor mode |
| MACS tables | Maxwellian-averaged cross sections at tabulated $kT$ | astrophysics mode |
| TALYS | theoretical σ(E) and MACS | filling channels missing from evaluations |
| `user_db/` | your own values | corrections and new data, see {doc}`../tutorials/custom-data` |

## Check that the data are found

1. Start the application. The terminal lists what was loaded, for example the user database entries and the libraries found.
2. In *Periodic Table*, click an element, then an isotope you know well (Co-60, Cs-137, Pb-209).
3. Check that its half-life and decay channels appear.

If nothing appears, see {ref}`troubleshooting-data`.

Next: {doc}`first-calculation`.
