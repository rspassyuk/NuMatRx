# Export and sessions

## Export numbers

| What | Where | Format |
|---|---|---|
| Isotope table of the network | Results → Isotopes & Matrix → **Export CSV** | CSV |
| Evolution | Results → Evolution → **csv** / **txt** | times, inventories, fractions, sums over $A$ |
| Equilibrium scan | Results → Equilibrium → **Export CSV** | flux, time, heat, inventories |
| Trajectory average | averaging panel → **Export averaged results** | CSV/TXT with a JSON header of all parameters and diagnostics |
| Nuclear data of one isotope | Periodic Table → **Save DecayData** / **Save NReactionData** | text |
| Full burnup matrix | Python API: `BurnupMatrix.export_txt()` | text |

## Sessions

A session (`.kaz` file) stores a finished calculation so you can look at it again later:

- the evolution run (times, inventories, heat, initial composition, settings),
- its trajectory average, if any,
- the equilibrium scan, if any,
- the material density used for W/cm³.

**Save…** writes the current results. **Open…** shows a session in a **separate window**, so you can compare it with the run you are working on, or open several sessions side by side.

A session is a record of results, not a project file: it does not restore the chart selection or all panel settings, and it is not recalculated when opened.

```{warning}
Sessions use Python's *pickle* format. Open only session files from people you trust.
```

## Sharing a result

For a result someone else can reproduce, send the numerical export together with the settings that produced it. The checklist is in {doc}`../reference/reproducibility`.
