# Nuclear data setup

NuMatRx reads externally installed nuclear data. It does not download a complete database automatically. Obtain evaluated files from their distributing institutions and retain the release identifiers and usage terms. See [source links](references.md#nuclear-data-sources).

## Where to put xsdir

The desktop service first checks `xsdir/` inside the project. If that directory does not exist, it checks for a sibling `xsdir/` beside the project. A present but incomplete project-local folder takes precedence over the sibling folder.

```text
workspace/
  NuMatRx/
    model/
    core/
    user_db/                 # optional private overrides
  xsdir/                     # shared external libraries
    endf-6/
    MACS/
```

Alternatively, place `xsdir/` directly inside `NuMatRx/`. The numerical quick start does not need either arrangement.

## Expected contents

```text
xsdir/
  endf-6/
    ENDFB-VIII.0/
      decay/
      neutrons/
  MACS/
    rawmacs.txt
    ENDFB71-EAF2010/
      ENDFB71/
      EAF2010/
  TALYS/
    recommended-ng-cross-sections/
    recommended-na-cross-sections/
    recommended-np-cross-sections/
    talys_macs_30_keV/
```

`endf-6` and `MACS` are required initialization directories. The GUI defaults to the `ENDFB-VIII.0` library name. Other evaluated-library folders and optional sources depend on your installation. Do not simply rename an unrelated distribution to match the default: choose and record the actual evaluation. Empty folders satisfy no physical data requirement.

## Verify loaded data

1. Start the application and inspect initialization messages in the terminal.
2. Open the nuclear-data registry and select an isotope with known records.
3. Confirm that its half-life and channels appear under the intended library.
4. Build a small network, then inspect the rates in Results before running Evolution.
5. Record source fallbacks and missing records. A missing evaluation is not evidence for a zero physical rate.

## Pointwise data and MACS

Reactor mode requests cross sections at a neutron energy; the astrophysical route prefers Maxwellian-averaged cross sections (MACS) at a thermal energy. A pointwise value at 30 keV is not automatically the MACS at `kT = 30 keV`. In fields labelled eV, 30 keV is entered as `30000`; in fields labelled keV, enter `30`.

Decay, pointwise-reaction, and MACS sources have different lookup routes. MACS fallback can combine user values, raw tables, multi-temperature tables, TALYS, and ENDF-derived averages. Record both the selected sources and their priority; the resulting network may contain rates from multiple evaluations.

## User overrides

Local overrides belong in `user_db/`. Inspect the bundled example under `examples/user_db/spectra/` and the reader in `nuclear_data/user_reader.py` before extending the schema. Keep supplied examples separate from your scientific dataset.

| Field or quantity | Unit / meaning |
|---|---|
| Half-life | Seconds |
| Branch fraction | Fraction, not percent |
| `Q_MeV` | Channel energy in MeV |
| `kT_keV`, `sigma_mb` | MACS thermal energy and millibarn cross section |
| CSV `E_eV`, `sigma_barn` | Pointwise energy and barn cross section |

For every override, record its source, affected isotope/state, channel, and uncertainty when available. An unknown energy should not be presented as a measured zero. Missing energies limit heat calculations even if isotope evolution can be computed. Reload/restart and verify that the intended value actually reaches the matrix.

The public repository excludes `xsdir/` and private `user_db/` contents. Documentation builds require neither dataset.
