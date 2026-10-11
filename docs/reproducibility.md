# Reproducibility

A saved plot, a reopened session, and a repeatable calculation are different deliverables. Sessions retain previously calculated results; reopening one does not execute a newer solver.

## Run record

For each scientific calculation save:

| Item | Required detail |
|---|---|
| Software | Git commit or release; whether local modifications were present |
| Environment | Python, NumPy and SciPy versions; operating system |
| Data | Evaluations, release identifiers, file checksums when possible, fallback order, private overrides |
| Network | Ordered isotope/state list, links, reaction MT and decay filters, manual channels, boundaries |
| Initial conditions | Complete isotope-resolved vector and its units |
| Irradiation | Flux or density conversion, pointwise energy or MACS kT, final time |
| Numerics | Solver, tolerances where configurable, saved time grid |
| Averaging | Distribution, parameter, integration range, diagnostics |
| Presentation | Normalization, filters, mass range, isotope aggregation |

Use `git rev-parse HEAD` and `git status --short` to record the revision and uncommitted changes. Do not assign a new solver revision to an old exported trajectory without rerunning it.

## Verification and comparison

- Compare the numerical engine with analytical chains and an independent solver on suitable small networks.
- Check both internal solver accuracy and quadrature convergence; they are separate.
- Inspect total inventory with the actual reaction stoichiometry and network boundaries.
- For literature comparisons document matched or differing isotope sets and all normalizations.

Keep an input manifest beside numerical exports and sessions. Screenshots support explanation of the workflow; they do not carry every input required for reproduction.
