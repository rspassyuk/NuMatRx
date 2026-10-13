# Installation check

**Goal:** check the numerical installation before loading nuclear libraries. This optional command-line check is for a source installation; installer users can proceed directly to the {doc}`first-gui-run` after configuring `xsdir`.

## Run the check

From the repository folder, after {doc}`installation`:

::::{tab-set}
:::{tab-item} Windows (PowerShell)
```powershell
.\.venv\Scripts\python.exe examples/documentation_quickstart.py
```
:::
:::{tab-item} Linux / macOS
```bash
.venv/bin/python examples/documentation_quickstart.py
```
:::
::::

No `xsdir` is needed. Successful completion prints `"passed": true`; a failed numerical check raises an error. Use `--output my_folder` to select an output directory.

## What is checked?

A synthetic chain $X_1 \rightarrow X_2$ has rate $\lambda=1\ \mathrm{s}^{-1}$, a stable daughter, and initial inventories $(1,0)$. Its exact solution is

$$N_1(t)=e^{-t},\qquad N_2(t)=1-e^{-t}.$$

At 2 s the inventories are approximately **0.1353352832** and **0.8646647168**. The script compares Padé, CRAM-16, adaptive CRAM-16 and CRAM-48 with this solution. It also checks the uniform average over 0–2 s: approximately **0.4323323584** and **0.5676676416**.

```{note}
Fe-56 and Co-56 are technical labels in this synthetic test. The assigned decay rate and daughter stability are artificial; this is not a physical Fe–Co decay calculation.
```

The assertions use relative/absolute comparison tolerances of `1e-9`/`2e-12` for propagation and an absolute tolerance of `5e-8` for the trapezoidal average. These are test thresholds, not solver settings.

## Output

- `results/documentation_quickstart/evolution.csv`: inventories from each solver.
- `results/documentation_quickstart/verification.json`: errors, averaged inventories and pass status.

Passing checks this small numerical example. GUI startup and nuclear-data loading are exercised separately in the {doc}`first-gui-run`.

::::{dropdown} Full verification script
```{literalinclude} ../../examples/documentation_quickstart.py
:language: python
```
::::
