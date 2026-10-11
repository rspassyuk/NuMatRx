# Simple decay chain

Run the [quick-start script](../quickstart.md) and inspect its `verification.json`. This is a controlled test of the backend with a known analytical solution.

## Exercises

1. Compare the four solver errors reported for the same chain and times.
2. Increase the final comparison time and check that the parent decreases and the stable daughter approaches one.
3. Change the uniform-average interval in both the grid and configuration. Update the analytical integral before comparing.
4. Double the number of uniformly spaced samples and compare the quadrature error. The output-time grid controls averaging resolution.

Do not replace the artificial rates by database values while keeping the same expected result: that would be a different model.
