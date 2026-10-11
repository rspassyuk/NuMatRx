# Cross sections and data sources

## Two kinds of reaction rate

A reaction rate per nucleus is $\lambda_n = \langle \sigma v \rangle\, n_n$. How $\langle\sigma v\rangle$ is evaluated depends on the neutron spectrum.

**Reactor mode — pointwise cross sections.** For neutrons of one energy $E$, $\lambda_n = \sigma(E)\,\Phi$. NuMatRx reads $\sigma(E)$ from the ENDF-6 neutron sublibrary (file MF=3) and interpolates it at the chosen energy: thermal 0.0253 eV, 1 keV, 1 MeV, 14.1 MeV (DT fusion) or any value you type.

**Astrophysics mode — Maxwellian-averaged cross sections.** In a star the neutrons have a Maxwell–Boltzmann distribution at temperature $T$. The relevant quantity is the MACS

$$
\langle\sigma\rangle_{kT} = \frac{2}{\sqrt\pi}\,\frac{1}{(kT)^2}\int_0^\infty \sigma(E)\,E\,e^{-E/kT}\,dE ,
$$

and the rate is $\lambda_n = \langle\sigma\rangle_{kT}\,\Phi$ with $\Phi = n_n v_T$ (Bao et al. 2000). NuMatRx takes MACS from tabulated sources at the chosen $kT$, typically 30 keV for the *s*-process.

```{important}
$\sigma(E = 30\ \mathrm{keV})$ and $\langle\sigma\rangle_{kT = 30\ \mathrm{keV}}$ are different numbers. Use reactor mode for monoenergetic neutrons and astrophysics mode for thermal stellar plasmas.
```

## Where the numbers come from

| Quantity | Sources | Default order |
|---|---|---|
| Half-lives, decay branches, decay energies | user database, ENDF-6 decay sublibrary (MF=8, MT=457) | user → ENDF-6 |
| Pointwise σ(E), isomeric branching | user CSV spectra, ENDF-6 neutron sublibrary (MF=3, MF=9/10), TALYS | — |
| MACS | user database, `rawmacs.txt`, ENDF/B-VII.1 and EAF-2010 multi-temperature tables, TALYS at 30 keV, MACS computed from ENDF σ(E) | user → rawmacs → ENDF/B-VII.1 → EAF-2010 → TALYS → computed from ENDF |

For each quantity NuMatRx walks down the priority list and takes the **first source that has a value**. You choose which sources take part in the source lists of the *Isotope Chart*; in Python you set the full order with `macs_priority=` and `dec_priority=` of `NuclearDataProvider`.

As a result, a network usually combines several libraries — for example rawmacs for stable lead isotopes, EAF-2010 for Pb-209 and TALYS for short-lived nuclides. The *Source* column in *Results → Isotopes & Matrix* (and `ReactionLink.source` in Python) records which library supplied each cross section. Report these sources together with your results.

## Missing data

If no source has a value, the link is not created and the nuclide is listed as having missing data. This means only that the installed libraries do not contain it — not that the reaction does not happen. Fill the gap through the user database ({doc}`../tutorials/custom-data`) or by adding a library to the priority list.

## Libraries

| Library | Type |
|---|---|
| ENDF/B-VIII.0 (default), JEFF, JENDL, TENDL | evaluated ENDF-6 libraries: decay and neutron data |
| ENDF/B-VII.1 MACS, EAF-2010 MACS | multi-temperature MACS tables |
| rawmacs | MACS table at standard temperatures |
| TALYS | theoretical nuclear-reaction model results |
