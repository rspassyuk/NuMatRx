# Reproducible results

A figure alone cannot be recalculated. To let others — or yourself in a year — reproduce a NuMatRx result, keep a short record next to the exported numbers.

## Checklist

| Item | Example |
|---|---|
| NuMatRx revision | `git rev-parse --short HEAD` → `2d5e302`; note uncommitted changes (`git status`) |
| Environment | Python 3.12, NumPy 2.1, SciPy 1.14, Windows 11 |
| Nuclear data | ENDF/B-VIII.0 decay; MACS priority user → rawmacs → ENDF/B-VII.1 → EAF-2010 → TALYS; contents of `user_db/` |
| Network | list of nuclides; MT filter; decay modes; half-life preset; manual channels; open/closed boundaries |
| Initial composition | Fe-56 = 1, all others 0 (and its units) |
| Irradiation | astrophysics mode, $kT$ = 30 keV, $\Phi = 2.5\times10^{16}$ n/cm²/s, end time $10^{15}$ s |
| Numerics | solver; number of saved times |
| Averaging | exponential exposure, $\tau_0$ = 0.3 mbarn⁻¹; tail and weight error |
| Presentation | normalisation (e.g. to Sm-150), plotted mass range |

## Tips

- The export of an average already contains its parameters and diagnostics in the header line.
- A `.kaz` session is convenient for looking at results again, but it does not record the whole set-up — keep the checklist as well.
- When you compare two runs, change one thing at a time and save a session for each.
- Cite the nuclear-data libraries you used, not only NuMatRx.
