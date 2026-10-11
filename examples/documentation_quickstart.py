"""Synthetic solver and averaging checks; no xsdir, GUI, or evaluated data."""
import argparse
import csv
import json
import platform
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from core.entities import Isotope, DecayLink
from core.burnup import BurnupConfig, BurnupMatrix
from core.exposure import ExposureConfig, average_exposure


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('results/documentation_quickstart'))
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    # Artificial kinetics: these are NOT evaluated Fe-56 / Co-56 properties.
    parent, daughter = Isotope(26, 'Fe', 56), Isotope(27, 'Co', 56)
    parent.decay_constant = 1.0
    parent.half_life_s = float(np.log(2.0))
    parent.add_decay(DecayLink('beta-', 1.0, 0.0, 1, 0, product=daughter))
    matrix = BurnupMatrix([parent, daughter], BurnupConfig(flux=0.0))
    matrix.build()
    initial = np.array([1.0, 0.0])
    times = np.array([0.0, 0.5, 1.0, 2.0, 5.0])
    expected = np.column_stack((np.exp(-times), -np.expm1(-times)))
    errors, rows = {}, []
    for method in ('pade', 'cram16', 'cram16_adaptive', 'cram48'):
        trajectory = np.array([matrix.solve(initial, float(t), method) for t in times])
        np.testing.assert_allclose(trajectory, expected, rtol=1e-9, atol=2e-12)
        errors[method] = float(np.max(abs(trajectory - expected)))
        rows.extend((method, float(t), *values) for t, values in zip(times, trajectory))

    grid = np.linspace(0.0, 2.0, 2001)
    trajectory = [matrix.solve(initial, float(t), 'cram16') for t in grid]
    averaged = average_exposure(matrix.names(), grid, trajectory, 0.0,
                               ExposureConfig(mode='time_uniform', start_s=0.0, end_s=2.0),
                               metadata={'constant_conditions': True, 'method': 'cram16',
                                         'synthetic': True})
    expected_mean = np.array([-np.expm1(-2.0) / 2.0, 1.0 + np.expm1(-2.0) / 2.0])
    np.testing.assert_allclose(averaged.mean, expected_mean, rtol=0.0, atol=5e-8)
    with (args.output / 'evolution.csv').open('w', newline='', encoding='utf-8') as handle:
        writer = csv.writer(handle)
        writer.writerow(['method', 'time_s', 'synthetic_parent', 'synthetic_daughter'])
        writer.writerows(rows)
    report = {'passed': True, 'synthetic': True, 'python': platform.python_version(),
              'maximum_absolute_errors': errors, 'mean_inventory': averaged.mean.tolist(),
              'mean_maximum_absolute_error': float(np.max(abs(averaged.mean - expected_mean)))}
    (args.output / 'verification.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))
    print(f'Outputs: {args.output.resolve()}')


if __name__ == '__main__':
    main()
