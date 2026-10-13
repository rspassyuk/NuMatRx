"""Eight-nuclide Pb--Bi--Po GUI companion; requires evaluated data in xsdir."""
import argparse
import csv
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from core import BurnupConfig, BurnupMatrix, IsotopeBuilder
from nuclear_data import EndfPathHolder, NuclearDataProvider

MACS_PRIORITY = ['rawmacs', 'endfb71', 'eaf2010', 'talys', 'endf_computed']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--xsdir', type=Path, help='Nuclear-data directory')
    parser.add_argument('--output', type=Path, default=Path('results/quickstart_pb_po'))
    args = parser.parse_args()
    xsdir = args.xsdir or next((p for p in (ROOT / 'xsdir', ROOT.parent / 'xsdir')
                               if p.is_dir()), ROOT / 'xsdir')
    EndfPathHolder.init_xsdir(str(xsdir))
    provider = NuclearDataProvider(
        dec_dir=EndfPathHolder.set_DEFAULT_DEC_DIR('ENDFB-VIII.0'),
        neu_dir=EndfPathHolder.set_DEFAULT_NEU_DIR('ENDFB-VIII.0'),
        macs_file=EndfPathHolder.set_DEFAULT_MACS_DIR('Endfb7'), macs_lib='Endfb7',
        endfb71_macs_dir=str(EndfPathHolder.get_ENDFB71_MACS_DIR()),
        eaf2010_macs_dir=str(EndfPathHolder.get_EAF2010_MACS_DIR()),
        talys_dir=str(EndfPathHolder.get_TALYS_DIR()),
        dec_priority=['endf6'], macs_priority=MACS_PRIORITY,
    )
    specs = [(82, 'Pb', a) for a in range(206, 211)]
    specs += [(83, 'Bi', 209), (83, 'Bi', 210), (84, 'Po', 210)]
    isotopes = IsotopeBuilder(provider).build_range(
        specs, E_eV=30000.0, mt_filter=[102], prefer_macs=True)
    config = BurnupConfig(flux=1e14)
    config.enable_specific_reactions([102])
    config.set_decay_time_filter('all')
    config.set_open_boundary_mts([102])
    matrix = BurnupMatrix(isotopes, config)
    matrix.build()
    names = matrix.names()
    initial = np.zeros(len(names))
    initial[names.index('Pb-206')] = 1.0
    channels = []
    edges = set()
    for isotope in isotopes:
        for link in isotope.getListOfReactions():
            daughter = getattr(link.product, 'name', '')
            channels.append(dict(parent=isotope.name, daughter=daughter,
                                 kind='capture', value=float(link.sigma_barn or 0),
                                 unit='barn', source=str(getattr(link, 'source', ''))))
            if link.mt == 102 and float(link.sigma_barn or 0) > 0 and daughter:
                edges.add((isotope.name, daughter))
        for link in isotope.getListOfDecays():
            daughter = getattr(link.product, 'name', '')
            rate = float(isotope.decay_constant or 0) * float(link.branch)
            channels.append(dict(parent=isotope.name, daughter=daughter,
                                 kind=str(link.mode), value=rate,
                                 unit='1/s', source='ENDFB-VIII.0'))
            if rate > 0 and daughter:
                edges.add((isotope.name, daughter))
    cycle = ['Pb-206', 'Pb-207', 'Pb-208', 'Pb-209', 'Bi-209', 'Bi-210', 'Po-210', 'Pb-206']
    missing = [f'{a} -> {b}' for a, b in zip(cycle, cycle[1:]) if (a, b) not in edges]
    if missing:
        raise RuntimeError('Required cycle links missing; check libraries and state branches: ' + ', '.join(missing))
    times = np.r_[0.0, np.geomspace(1e-6, 1e14, 399)]
    # Same independent propagation from N(0) as the GUI output grid.
    trajectory = np.array([matrix.solve(initial, float(t), 'cram16') for t in times])
    if not np.isfinite(trajectory).all() or trajectory.min() < -1e-10:
        raise RuntimeError('Non-finite or significantly negative inventories; inspect the matrix.')
    args.output.mkdir(parents=True, exist_ok=True)
    with (args.output / 'evolution.csv').open('w', newline='', encoding='utf-8') as handle:
        writer = csv.writer(handle)
        writer.writerow(['time_s', *names])
        writer.writerows(zip(times, *trajectory.T))
    with (args.output / 'channels.csv').open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=['parent', 'daughter', 'kind', 'value', 'unit', 'source'])
        writer.writeheader()
        writer.writerows(channels)
    matrix.export_txt(str(args.output / 'matrix.txt'), mode='total')
    report = dict(method='cram16', flux_n_cm2_s=1e14, kT_keV=30,
                  end_time_s=1e14, n_points=400, t_start_s=1e-6,
                  initial={'Pb-206': 1.0}, isotope_names=names,
                  decay_library='ENDFB-VIII.0', rawmacs_library='Endfb7',
                  macs_priority=MACS_PRIORITY, user_overrides=False,
                  open_boundary_mts=[102], missing_cross_sections=matrix.missing,
                  final_inventory=dict(zip(names, trajectory[-1].tolist())),
                  final_total=float(trajectory[-1].sum()), minimum=float(trajectory.min()))
    (args.output / 'settings.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(9, 5), layout='constrained')
    for i, name in enumerate(names):
        # Nonpositive values cannot be shown on a logarithmic axis; CSV is unchanged.
        ax.plot(times[1:], np.where(trajectory[1:, i] > 0, trajectory[1:, i], np.nan), label=name)
    ax.set(xscale='log', yscale='log', xlabel='Time [s]', ylabel='Inventory N',
           title='Pb--Bi--Po quick start: kT = 30 keV, flux = 1e14 n/cm²/s')
    # Focus the illustration on populated inventories; CSV retains the entire grid.
    ax.set_xlim(1e8, 1e14)
    ax.set_ylim(1e-14, 2)
    ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1.0))
    ax.grid(alpha=0.2)
    fig.savefig(args.output / 'concentrations.png', dpi=180)
    plt.close(fig)
    print(json.dumps(report, indent=2))
    print(f'Outputs: {args.output.resolve()}')


if __name__ == '__main__':
    main()
