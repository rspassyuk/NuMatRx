# Export and saved sessions

A `.kaz` file stores Evolution, the attached average, optional equilibrium results and density. Open it in a separate result window without replacing the live workspace. Multiple sessions can be inspected side by side.

Sessions are result archives, not a full editable GUI snapshot: sensitivity scans, unsaved widget settings and every workspace edit are not restored. Existing trajectories are not recalculated on opening. The format uses Python pickle, so open only trusted session files.

Save plot images from the Matplotlib toolbar. Numerical exports and figures are separate artifacts. Include their metadata and initial conditions when sharing a scientific result.

## Share a reproducible run

Include the numerical export, initial vector, matrix membership, enabled channels, irradiation settings, source priorities, data versions, software revision, and averaging settings. A session is useful for viewing results, but it is not a replacement for this manifest. See [Reproducibility](../reproducibility.md).
