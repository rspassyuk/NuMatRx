# Network: nuclides and links

A NuMatRx network is a list of {py:class}`~core.entities.Isotope` objects. Each isotope owns its outgoing decay and reaction links, and each link points to the daughter isotope. The burnup matrix is built from these links.

| Class | Purpose |
|---|---|
| {py:class}`~core.entities.Isotope` | one nuclide (ground or isomeric state) with its outgoing links |
| {py:class}`~core.entities.DecayLink` | one decay channel: mode, branch, energy, daughter |
| {py:class}`~core.entities.ReactionLink` | one neutron reaction: MT, effective cross section, daughter |
| {py:class}`~core.entities.Element`, {py:class}`~core.entities.ChemTable` | chemical element and the Z ↔ symbol table |
| {py:class}`~core.registry.IsotopeBuilder` | builds and links isotopes from a {py:class}`~nuclear_data.provider.NuclearDataProvider` |

## Nuclides and links — `core.entities`

```{py:module} core.entities
```

::::{py:class} Isotope(Z, X, A, meta=None)

A nuclide that can be filled with data from a library or by hand. The burnup matrix needs only the attributes listed here, so a network can be built without any data files.

:param Z: proton number; must match the symbol `X`.
:type Z: int
:param X: chemical symbol, e.g. `"Pb"`.
:type X: str
:param A: mass number, `A > 0`.
:type A: int
:param meta: isomeric state: `None` for the ground state, `1` for the first isomer.
:type meta: int or None
:raises ValueError: if `A <= 0` or `Z` and `X` do not match.

```{py:attribute} half_life_s
:type: float | None

Half-life in seconds; `None` for a stable nuclide.
```

```{py:attribute} decay_constant
:type: float

Decay constant λ in s⁻¹ (0 for stable nuclides). This value enters the matrix; `half_life_s` is informative.
```

```{py:attribute} mass
:type: float | None

Atomic mass in u, if known.
```

```{py:property} name
:type: str

Canonical label such as `"Pb-206"` or `"Bi-210m1"`. Used everywhere as the nuclide name.
```

```{py:method} from_symbol(X, A, meta=None)
:classmethod:

Create an isotope from its symbol; `Z` is looked up in {py:class}`ChemTable`.

:rtype: Isotope
```

```{py:method} add_decay(link)

Append an outgoing {py:class}`DecayLink`.
```

```{py:method} add_reaction(link)

Append an outgoing {py:class}`ReactionLink`.
```

```{py:method} getListOfDecays()

:returns: the outgoing decay links.
:rtype: list[DecayLink]
```

```{py:method} getListOfReactions()

:returns: the outgoing reaction links.
:rtype: list[ReactionLink]
```

Two isotopes are equal if `Z`, `A` and `meta` are equal, so isotopes can be used as dictionary keys.

**Example**

```python
from core.entities import Isotope, DecayLink

sr, y = Isotope(38, "Sr", 90), Isotope(39, "Y", 90)
sr.half_life_s = 9.08e8
sr.decay_constant = 0.6931 / sr.half_life_s
sr.add_decay(DecayLink("beta-", 1.0, 0.546, 1, 0, product=y))
print(sr.name, sr.getListOfDecays())   # Sr-90 [DecayLink(beta-, BR=1, dZ=1, dA=0)]
```
::::

::::{py:class} DecayLink(mode, branch, Q_MeV, dz, da, rfs=0, product=None)

One decay channel of a parent nuclide.

:param mode: decay mode, e.g. `"beta-"`, `"alpha"`, `"ec/beta+"`, `"it"`.
:type mode: str
:param branch: branching fraction (0–1, not percent).
:type branch: float
:param Q_MeV: energy released in this channel, MeV; used for heat release.
:type Q_MeV: float
:param dz: change of proton number (β⁻: `+1`, α: `-2`).
:type dz: int
:param da: change of mass number (α: `-4`).
:type da: int
:param rfs: final isomeric state of the daughter (0 = ground state).
:type rfs: int
:param product: daughter isotope; `None` means the decay leaves the network.
:type product: Isotope or None

A decay to a product outside the network is always kept and acts as a loss (sink).
::::

::::{py:class} ReactionLink(mt, name, sigma_barn, q_yield=1.0, Q_MeV=0.0, lfs=0, product=None, source=None)

One neutron-induced reaction of a parent nuclide.

:param mt: ENDF reaction number (102 for (n,γ)).
:type mt: int
:param name: readable label, e.g. `"(n,γ)"`.
:type name: str
:param sigma_barn: effective cross section in barn at the working energy or temperature. For links built by {py:class}`~core.registry.IsotopeBuilder` it already includes the isomeric yield.
:type sigma_barn: float
:param q_yield: fraction going to this final state.
:type q_yield: float
:param Q_MeV: reaction energy, MeV; used for heat release.
:type Q_MeV: float
:param lfs: final isomeric state of the product.
:type lfs: int
:param product: product isotope; `None` if it is not in the network.
:type product: Isotope or None
:param source: name of the data source that supplied `sigma_barn` (`"rawmacs"`, `"eaf2010"`, `"talys"`, …).
:type source: str or None

```{py:method} getId()

:returns: the MT number.
:rtype: int
```
::::

::::{py:class} Element(Z, X)

A chemical element. Base class of {py:class}`Isotope`.

:raises ValueError: if `Z` is unknown or does not match `X`.
::::

::::{py:class} ChemTable

Periodic table lookup.

```{py:method} Z_of(symbol)
:staticmethod:

:returns: the proton number for a chemical symbol.
:rtype: int
```
::::

## Building networks from data — `core.registry`

```{py:module} core.registry
```

::::{py:class} IsotopeBuilder(provider)

Creates isotopes from nuclear data and links each decay and reaction to its daughter.

:param provider: the data source.
:type provider: ~nuclear_data.provider.NuclearDataProvider

```{py:method} build_isotope(Z, X, A, meta=None, E_eV=0.0253, mt_filter=None, audit=None, prefer_macs=False)

Create one isotope with its decay channels and neutron reactions (products are not linked yet).

:param E_eV: neutron energy (reactor mode) or thermal energy kT (astrophysics mode), in eV.
:param mt_filter: load only these MT channels; `None` loads all available.
:type mt_filter: list[int] or None
:param audit: if a dict is given, the data provenance is written into it.
:type audit: dict or None
:param prefer_macs: `True` takes Maxwellian-averaged cross sections at kT = `E_eV` first and falls back to pointwise σ(E); `False` uses pointwise σ(E).
:type prefer_macs: bool
:rtype: ~core.entities.Isotope
```

```{py:method} build_range(specs, E_eV=0.0253, mt_filter=None, prefer_macs=False)

Build a list of isotopes and link all products inside the list.

:param specs: tuples `(Z, X, A)` or `(Z, X, A, meta)`.
:type specs: list[tuple]
:returns: linked isotopes, in the order of `specs`.
:rtype: list[~core.entities.Isotope]
```

```{py:method} missing_isotopes()

:returns: names of isotopes for which no decay or reaction data were found.
:rtype: list[str]
```

```{py:method} print_report()

Print a table: isotope, decay source, reaction sources.
```

```{py:method} link_products(isotopes)
:staticmethod:

Set `product` on every decay and reaction link by matching Z, A and isomeric state inside `isotopes`.
```

**Example**

```python
from core import IsotopeBuilder

builder = IsotopeBuilder(provider)
isotopes = builder.build_range(
    [(82, "Pb", 208), (82, "Pb", 209), (83, "Bi", 209)],
    E_eV=30_000.0, mt_filter=[102], prefer_macs=True)
builder.print_report()
```
::::
