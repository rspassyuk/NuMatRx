# Troubleshooting

## Application or data initialization fails

Run `python model/core.py` with the environment used to install dependencies. Inspect the full terminal error. Check `xsdir/endf-6`, `xsdir/MACS`, the selected library folders, and the `endf` dependency. A project-local `xsdir` takes precedence over a sibling folder even when incomplete. See [data setup](nuclear-data.md).

## CRAM refinement fails

Messages about non-convergence or step-size resolution mean that adaptive acceptance failed; they do not identify a physical cause by themselves. Record the complete message, time range, initial vector, matrix/network settings, and source revision. Compare manageable cases with Padé and CRAM-48 and inspect the enabled rates and boundary loss.

Local development versions may contain numerical fixes that are not yet in a downloaded release. Use the actual revision and restart after changing code. Do not identify version compatibility from the application name alone. If available, retain the reported error estimate, minimum inventory, inventory totals, and failing isotope index together with the ordered isotope list.

Reducing the output-grid spacing is not the same as changing the adaptive solver's internal steps. Do not remove numerical checks or clip values to make a failed run appear valid.

## Averaging fails after ordinary CRAM-16

Averaging is not restricted to the adaptive solver. It validates trajectory shape, finite values, time ordering, initial inventory, and negative values. Earlier error messages may specifically recommend adaptive CRAM-16; this is not a guarantee that it will resolve every network.

Check the named isotope and time in the message. Recalculate Evolution after changing the solver. Opening an old session or changing a dropdown alone does not change the stored concentrations. Signed numerical residual handling can differ between revisions; include the revision in an issue report.

## Empty or discontinuous plot

Check the plot type, source (**Time slice** or **Averaged results**), isotope filter, display threshold, and whether the relevant calculation finished. Logarithmic axes cannot show zero or negative values. Missing capture cross sections can produce gaps in sigma-N plots. See [plotting](user-guide/plotting.md).

## Abundance curve changes between time and exposure averages

The weighting prescriptions differ. Exponential time and exposure averages are equivalent only for the same constant-flux trajectory with matched mean parameters. A uniform time average generally produces a different curve. See [averaging](user-guide/averaging.md).

## Averaging has high coverage but an inaccurate weight integral

Coverage estimates the included distribution range. The numerical weight integral also depends on grid spacing. Refine saved times via `n_points` in the service API and repeat the calculation; extend the integration range separately. Retain both diagnostics.

## Inventory decreases or boundary ratios become large

Inspect daughters outside the selected matrix, per-MT open channels, decays, and missing links. A small reference abundance can produce a large ratio. Normalizing the curve does not repair material lost from a truncated network.

## Cycle search stops early

The search has time, length, and result-count limits. A partial list is expected for sufficiently connected graphs. Narrow the selected nuclides/channels and inspect the status. Closed connectivity does not measure the physical circulation rate.

## Plot export fails with TeX or font errors

Keep the numerical export: a rendering failure is distinct from a solver failure. Record the Matplotlib/TeX error and installed versions. External TeX rendering may require a correctly configured local TeX installation. Sphinx HTML documentation itself does not need a desktop TeX installation.

## Reporting a problem

Provide the command or GUI action, full traceback, revision, Python/dependency versions, solver, initial vector, isotope list, irradiation settings, and a minimal input reproducing the issue. Describe private data by release and source where possible rather than uploading restricted libraries. Use the repository's [issue tracker](https://github.com/rspassyuk/NuMatRx/issues).
