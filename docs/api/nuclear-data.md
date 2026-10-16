# Nuclear data

The `nuclear_data` package reads files and returns plain data objects. It knows nothing about burnup. In most scripts you only need {py:class}`~nuclear_data.path_holder.EndfPathHolder` to locate the libraries and {py:class}`~nuclear_data.provider.NuclearDataProvider` to query them; the readers are used inside the provider. File layout: {doc}`../reference/data-formats`.

| Object | Purpose |
|---|---|
| {py:class}`~nuclear_data.path_holder.EndfPathHolder` | finds and stores the folders of `xsdir/` |
| {py:class}`~nuclear_data.provider.NuclearDataProvider` | one interface over all sources, with priorities |
| {py:class}`~nuclear_data.endf_reader.EndfReader` | ENDF-6 decay and neutron data of one nuclide |
| {py:class}`~nuclear_data.macs_reader.MacsReader`, {py:class}`~nuclear_data.macs_reader.MultiMacsReader` | MACS tables |
| {py:class}`~nuclear_data.talys_reader.NreacTalys` | TALYS cross sections |
| {py:class}`~nuclear_data.user_reader.UserDataReader` | your own data in `user_db/` |
| {py:class}`~nuclear_data.models.DecayData` and others | the returned data objects |

Nuclide keys in MACS tables and in the user database have the form `"82-Pb-208"` (with `m1` for isomers).

## Paths — `nuclear_data.path_holder`

```{py:module} nuclear_data.path_holder
```

::::{py:class} EndfPathHolder

Stores the data folders as class-level settings; all methods are static.

```{py:method} init_xsdir(xsdir_path)
:staticmethod:

Register an `xsdir` folder. `endf-6/` and `MACS/` are required; `TALYS/` and the ENDF/B-VII.1 and EAF-2010 MACS folders are found automatically if present.

:returns: the discovered folders by name (`"xsdir"`, `"endf-6"`, `"MACS"`, `"TALYS"`, `"ENDFB71_MACS"`, `"EAF2010_MACS"`).
:rtype: dict[str, str]
:raises FileNotFoundError: if a required folder is missing.
```

```{py:method} set_DEFAULT_DEC_DIR(library)
:staticmethod:

Select the decay sublibrary `endf-6/<library>/decay`; returns its path.
```

```{py:method} set_DEFAULT_NEU_DIR(library)
:staticmethod:

Select the neutron sublibrary `endf-6/<library>/neutrons`; returns its path.
```

```{py:method} set_DEFAULT_MACS_DIR(library_alias, filename="rawmacs.txt")
:staticmethod:

Select the MACS file and the library column to read from it (e.g. `"Endfb7"`); returns the file path.
```

```{py:method} set_USER_DB_DIR(path)
:staticmethod:

Register the user database folder; returns its path.
```

The getters `get_DEFAULT_DEC_DIR()`, `get_DEFAULT_NEU_DIR()`, `get_macs_file()`, `get_macs_library()`, `get_ENDFB71_MACS_DIR()`, `get_EAF2010_MACS_DIR()`, `get_TALYS_DIR()` and `get_USER_DB_DIR()` return the current settings; `set_ENDFB71_MACS_DIR`, `set_EAF2010_MACS_DIR` and `set_TALYS_DIR` override the automatic search.
::::

## Provider — `nuclear_data.provider`

```{py:module} nuclear_data.provider
```

```{py:data} MACS_DEFAULT_PRIORITY
:value: ["user", "rawmacs", "endfb71", "eaf2010", "talys", "endf_computed"]

Default order of MACS sources. The default decay order is `["user", "endf6"]`.
```

::::{py:class} NuclearDataProvider(dec_dir=None, neu_dir=None, macs_file=None, macs_lib=None, user_dir=None, talys_dir=None, endfb71_macs_dir=None, eaf2010_macs_dir=None, macs_priority=None, dec_priority=None)

Queries every configured source and returns the first value found, in priority order. Sources that are not given are skipped.

:param dec_dir: ENDF-6 decay folder.
:param neu_dir: ENDF-6 neutron folder (σ(E), isomeric branching, MACS computed from σ(E)).
:param macs_file: `rawmacs.txt`; `macs_lib` selects the library column.
:param user_dir: user database folder.
:param talys_dir: TALYS root folder.
:param endfb71_macs_dir: multi-temperature MACS from ENDF/B-VII.1.
:param eaf2010_macs_dir: multi-temperature MACS from EAF-2010.
:param macs_priority: MACS source order; default {py:data}`MACS_DEFAULT_PRIORITY`.
:param dec_priority: decay source order; default `["user", "endf6"]`.

```{py:method} get_decay(Z, X, A, meta=None)

:returns: decay data from the first source that has them, or `None`.
:rtype: ~nuclear_data.models.DecayData or None
```

```{py:method} get_macs(Z, X, A, mt, kT_keV, meta=None)

:returns: the MACS at `kT_keV` (interpolated in tables with several temperatures), or `None`.
:rtype: ~nuclear_data.models.MacsPoint or None
```

```{py:method} get_macs_with_source(Z, X, A, mt, kT_keV, meta=None)

:returns: `(MacsPoint, source_name)` or `(None, None)`.
```

```{py:method} get_sigma(Z, X, A, mt, E, e_unit="eV", meta=None)

Pointwise cross section at energy `E`; priority user → ENDF → TALYS.

:returns: σ in barn, or `None`.
:rtype: float or None
```

```{py:method} get_sigma_with_source(Z, X, A, mt, E, e_unit="eV", meta=None)

:returns: `(sigma_barn, source_name)`.
```

```{py:method} get_isomeric_branches(Z, X, A, mt, E_eV, meta=None)

:returns: fractions going to each final state (ENDF only); `[LFS=0, yield=1.0]` if no data.
:rtype: list[~nuclear_data.models.IsomericBranch]
```

```{py:method} get_reaction_data(Z, X, A, mt, meta=None)

:returns: full reaction data; priority user → ENDF → TALYS.
:rtype: ~nuclear_data.models.NeutronReactionData or None
```

```{py:method} set_macs_priority(priority)

Change the MACS source order. `get_macs_priority()` returns it.
```

```{py:method} set_dec_priority(priority)

Change the decay source order. `get_dec_priority()` returns it.
```

```{py:method} reload_user_db()

Read `user_db/` again after editing it.
```

**Example**

```python
from nuclear_data import EndfPathHolder, NuclearDataProvider

EndfPathHolder.init_xsdir("xsdir")
nd = NuclearDataProvider(
    dec_dir=EndfPathHolder.set_DEFAULT_DEC_DIR("ENDFB-VIII.0"),
    neu_dir=EndfPathHolder.set_DEFAULT_NEU_DIR("ENDFB-VIII.0"),
    macs_file=EndfPathHolder.set_DEFAULT_MACS_DIR("Endfb7"), macs_lib="Endfb7",
    endfb71_macs_dir=str(EndfPathHolder.get_ENDFB71_MACS_DIR()),
    eaf2010_macs_dir=str(EndfPathHolder.get_EAF2010_MACS_DIR()),
    talys_dir=str(EndfPathHolder.get_TALYS_DIR()))

print(nd.get_decay(83, "Bi", 210).half_life_s)              # s
print(nd.get_macs_with_source(82, "Pb", 208, 102, 30.0))    # MACS in mb and its source
```
::::

## Readers

```{py:module} nuclear_data.endf_reader
```

::::{py:class} EndfReader(Z, X, A, meta=None, dec_dir=None, neu_dir=None)

ENDF-6 data of one nuclide: decay (MF=8, MT=457) and neutron reactions (MF=3, MF=9/10). Needs the `endf` package.

```{py:property} has_decay
:type: bool
```

```{py:property} has_neutron
:type: bool
```

```{py:method} get_decay_data()

:returns: decay data; a stable nuclide if no decay file is present.
:rtype: ~nuclear_data.models.DecayData
```

```{py:method} available_mts()

:returns: MT numbers with a cross-section section (MF=3).
```

```{py:method} get_cross_section(mt, e_unit="eV", cs_unit="barn")

:returns: the full σ(E) table.
:rtype: list[~nuclear_data.models.CrossSectionPoint]
```

```{py:method} get_sigma_at(mt, E, e_unit="eV")

:returns: σ in barn interpolated at `E`.
```

```{py:method} get_isomeric_branches(mt, E_eV)

:rtype: list[~nuclear_data.models.IsomericBranch]
```

```{py:method} get_reaction_data(mt)

:rtype: ~nuclear_data.models.NeutronReactionData
```

```{py:method} compute_macs(mt, kT=30.0, kT_unit="keV")

Integrate σ(E) over a Maxwell–Boltzmann distribution at `kT`.

:returns: the MACS in mb.
:rtype: ~nuclear_data.models.MacsPoint
```

```{py:method} get_mass(to_kg=False)

:returns: atomic mass in u (or kg).
```
::::

```{py:module} nuclear_data.macs_reader
```

::::{py:class} MacsReader(macs_file, library_alias)

Reads `rawmacs.txt`. `library_alias` selects the column: `"Endfb7"` (ENDF/B-VII.0), `"Endfb6"` (ENDF/B-VI.8), `"Jeff"` (JEFF-3.1) or `"Jendl"` (JENDL-3.3).

```{py:method} get_all_points(iso_key, mt)

:rtype: list[~nuclear_data.models.MacsPoint]
```

```{py:method} get_macs_at(iso_key, mt, kT_keV)

:returns: the MACS at `kT_keV`, interpolated between table temperatures.
:rtype: ~nuclear_data.models.MacsPoint or None
```
::::

::::{py:class} MultiMacsReader(directory)

Reads the multi-temperature MACS tables of ENDF/B-VII.1 or EAF-2010 (one directory each).

```{py:method} get_all_points(iso_key, mt=102)

:returns: all MACS(kT) points in mb.
```

```{py:method} get_macs_at(iso_key, mt, kT_keV)

:returns: the MACS interpolated at `kT_keV`.
```

```{py:method} available_isotopes()

:rtype: list[str]
```
::::

```{py:module} nuclear_data.talys_reader
```

::::{py:class} NreacTalys(talys_root, Z, X, A, meta=None)

TALYS cross sections of one nuclide.

```{py:method} available_mts()

:rtype: list[int]
```

```{py:method} get_cross_section(mt)

:returns: σ(E) with E in eV and σ in barn.
```

```{py:method} get_sigma_at(mt, E, e_unit="eV")
```

```{py:method} get_macs_30keV(mt=102)

:returns: the MACS at kT = 30 keV (only for MT=102), or `None`.
```

```{py:method} get_reaction_data(mt)
```
::::

```{py:module} nuclear_data.user_reader
```

::::{py:class} UserDataReader(db_dir)

Reads `user_db/isotopes.json` and `user_db/spectra/<key>_mt<MT>.csv`. Format: {doc}`../tutorials/custom-data`.

:raises FileNotFoundError: if `db_dir` does not exist.

```{py:method} reload()

Read the files again.
```

```{py:method} get_decay_data(Z, X, A, meta=None)
```

```{py:method} get_reaction_data(Z, X, A, mt, meta=None)
```

```{py:method} has_decay(Z, X, A, meta=None)
```

```{py:method} has_reaction(Z, X, A, mt, meta=None)
```

```{py:method} list_isotopes()

:returns: the keys present in `isotopes.json`.
```
::::

## Data objects — `nuclear_data.models`

```{py:module} nuclear_data.models
```

```{py:class} DecayChannel(mode, branch, Q_MeV, dz, da, rfs=0)

One decay channel: mode, branching fraction, energy (MeV), changes of Z and A, final state.
```

::::{py:class} DecayData(half_life_s, decay_constant, channels=[], source="unknown")

Decay data of one nuclide: half-life (s, `None` if stable), decay constant (s⁻¹), list of {py:class}`DecayChannel` and the source name.

```{py:property} is_stable
:type: bool
```
::::

```{py:class} CrossSectionPoint(E_eV, sigma_barn)

One point of a σ(E) table.
```

```{py:class} MacsPoint(kT_keV, sigma_mb, rate_cm3_mol_s=None)

One MACS value: temperature (keV), cross section (mb), optional reaction rate.
```

```{py:class} IsomericBranch(LFS, yield_)

Fraction `yield_` of a reaction going to final state `LFS`.
```

```{py:class} NeutronReactionData(mt, channel_name, Q_MeV, spectrum=[], macs=[], branches=[], source="unknown")

All data of one reaction of one nuclide: σ(E) `spectrum`, `macs` points, isomeric `branches`, reaction energy and source.
```
