# Periodic Table: inspecting nuclear data

Use this workspace before building a network: it shows exactly what the installed libraries contain for each isotope.


```{image} ../_static/images/registry.png
:alt: Periodic Table workspace
:class: screenshot
```

## Look up an isotope

1. Click an element in the periodic table.
2. Pick an isotope (ground or metastable state) from the list.
3. Read the two information panes:
   - **Decay data**: half-life, decay constant, decay modes with branching ratios and energies.
   - **Reaction data**: neutron reaction channels (MT numbers) and their cross sections.

## Compare libraries

Tick several libraries to see the same isotope in each of them. Differences in half-lives or cross sections between evaluations show up immediately — useful before you decide which library to use for a calculation.

## Export

**Save DecayData** and **Save NReactionData** write the displayed records to text files, without running any calculation.

```{tip}
If an isotope shows no data, it is not in the installed library — this does not mean the reaction does not happen. You can add missing values through the user database, see {doc}`../tutorials/custom-data`.
```
