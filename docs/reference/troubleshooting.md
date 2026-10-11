# Troubleshooting and FAQ

(troubleshooting-data)=
## The application starts, but no data appear

- Is there an `xsdir/` folder inside the project or next to it, with `endf-6/` and `MACS/` directly inside? A doubled `xsdir/xsdir/` is the most common mistake.
- Is the `endf` package installed? Install with `requirements-endf.txt`.
- Read the messages in the terminal: they show which folders were found.
- An `xsdir/` inside the project wins over one next to it, even if it is incomplete.

## Qt cannot start on Linux ("could not load the Qt platform plugin xcb")

Install your distribution's Qt runtime libraries (for example the `libxcb-*` packages), then start again. This is a system issue, not a NuMatRx one.

## A nuclide has no cross section

The installed libraries do not contain it at this energy or temperature. Options: add another source to the priority list (TALYS often fills gaps), or enter a value in the user database ({doc}`../tutorials/custom-data`).

## The total inventory decreases

Material leaves the network through open boundary channels or through decays into nuclides that are not selected. Look at **Results → Isotopes & Matrix → Open channels**, and add the daughters to the network if you need to follow them. See {doc}`../theory/network-equations`.

## "CRAM step refinement did not converge"

The adaptive solver could not meet its accuracy checks. Check the network for unusual rates (a cross section in the wrong unit, a half-life of zero), try a shorter end time, and compare with CRAM-48 or, for small networks, Padé. If the problem persists, report it with the details listed below.

## Averaging is blocked

The averaging panel refuses trajectories with significant negative values or invalid times. Recalculate the evolution with **CRAM-16 (adaptive)**, which never returns significant negative values. Note that changing the solver in the list does not change a saved run — calculate again.

## The averaged curve looks different from the time slice

They answer different questions: a time slice is one moment of one irradiation; an average mixes many. Exponential *time* and *exposure* averages agree only for the same constant-flux run with $t_0 = \tau_0/(10^{-27}\Phi)$.

## Gaps in σN plots

Nuclides without a capture cross section have no σN value and are left out. The averaging diagnostics list them under missing cross sections.

## The cycle search stops early

It reached its time, length or count limit; the status says so. Narrow the network or the selected channels, or raise the limits.

## The plot is empty

Check the graph type, the abundance source (**Time slice** / **Averaged results**), the nuclide filter and the display threshold. Logarithmic axes cannot show zero or negative values.

## Reporting a problem

Open an issue at <https://github.com/rspassyuk/NuMatRx/issues> with:

- what you did (GUI steps or script) and the full error message from the terminal;
- the NuMatRx revision (`git rev-parse --short HEAD`), Python and operating system;
- the network (list of nuclides), initial composition, flux, energy, end time and solver;
- the nuclear-data libraries and their priority.
