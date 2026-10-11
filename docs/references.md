# References and citation

## Citing a calculation

Cite the relevant project publication and the nuclear-data evaluations actually used. Include the software commit or release and the input manifest. This documentation does not assign a software DOI or invent a release number.

## Project publication

Kenzhebayev, N., Khassanov, M., Spassyuk, R., Anarbek, D., Aimuratov, Y., and Abishev, M. (2026). *Just Beyond the S-Process Termination Point: Nucleosynthesis of Lead–Bismuth Cyclic Reactions*. Galaxies 14, 46. [DOI: 10.3390/galaxies14030046](https://doi.org/10.3390/galaxies14030046).

The historical [nr-tool project](https://github.com/Nurzat-89/nr-tool) provides context for the earlier C# implementation. NuMatRx's network and interface examples should identify which version generated their results.

## Methods and reference distributions

- Pusa and Leppänen (2010), matrix-exponential burnup calculations using CRAM. [DOI: 10.13182/NSE09-14](https://doi.org/10.13182/NSE09-14).
- Pusa (2016), higher-order CRAM and incomplete partial factorization. [DOI: 10.13182/NSE15-26](https://doi.org/10.13182/NSE15-26).
- Virtanen et al. (2020), SciPy 1.0. [DOI: 10.1038/s41592-019-0686-2](https://doi.org/10.1038/s41592-019-0686-2).
- Arlandini et al. (1999), classical and stellar s-process reference abundances. [DOI: 10.1086/307938](https://doi.org/10.1086/307938).
- Käppeler, Beer, and Wisshak (1989), s-process nucleosynthesis review. [DOI: 10.1088/0034-4885/52/8/002](https://doi.org/10.1088/0034-4885/52/8/002).
- Koloczek et al. (2016), sensitivity study for s-process nucleosynthesis in AGB stars. [DOI: 10.1016/j.adt.2015.12.001](https://doi.org/10.1016/j.adt.2015.12.001).

Literature references motivate methods; they do not establish that every network selected in NuMatRx reproduces those calculations.

## Nuclear-data sources

- [NNDC ENDF](https://www.nndc.bnl.gov/endf/): evaluated nuclear data.
- [IAEA Nuclear Data Services](https://www-nds.iaea.org/): nuclear-data access and resources.
- [JENDL](https://wwwndc.jaea.go.jp/jendl/jendl.html): evaluated data releases from JAEA.

These are source portals, not a ready-made NuMatRx `xsdir` archive. Match the downloaded file formats and layout to the configured readers. Data remain subject to their own release conditions and attribution requirements.
