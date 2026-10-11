# Cycle analysis

Some reaction networks contain closed paths: a sequence of captures and decays that returns to the nuclide it started from. The best-known example is the Pb–Bi–Po cycle at the end of the *s*-process. NuMatRx finds such cycles automatically.

## The network as a graph

The cycle search treats the network as a directed graph:

- **vertices** — nuclides;
- **edges** — decay and reaction links from a parent to its daughter.

An **elementary cycle** is a closed path that visits no nuclide twice. Enumerating elementary cycles is a standard problem of graph theory (Johnson 1975; Hagberg et al. 2008).

## The algorithm

NuMatRx uses an iterative depth-first search. The vertices are put in a fixed order, and a cycle is only searched from its lowest-ranked vertex, so each cycle is found exactly once.

The number of cycles can grow very quickly with the size of the network, so the search is bounded:

| Limit | Purpose |
|---|---|
| maximum cycle length | ignore very long loops |
| maximum number of cycles | stop after enough examples |
| time limit | keep the application responsive |

The search can also be cancelled. When any limit stops it, the status says so and the list may be incomplete.

Each cycle is reported with its nuclides and the type of each step; the summary separates pure-decay, pure-reaction and mixed cycles.

## Interpreting a cycle

The search uses the links of the network, not the rates. A cycle therefore means that material **can** circulate along this path. How much actually does depends on the cross sections, half-lives and flux — run an evolution or an equilibrium calculation to find out. In the termination network of {doc}`../tutorials/termination-cycle`, 14 cycles are found. At a flux of $10^{14}$ n/cm²/s, Pb-209 β⁻-decays some $10^{8}$ times faster than it captures a neutron, so the branches through Pb-210 carry almost nothing and the flow follows the classical Pb-206 → … → Po-210 → Pb-206 loop.

## In Python

```python
from core import CycleAnalyzer

analyzer = CycleAnalyzer(isotopes)
cycles = analyzer.find_all_cycles(max_length=10, timeout_s=30)
analyzer.print_report(cycles)
```
