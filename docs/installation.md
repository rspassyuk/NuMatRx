# Installation

## Requirements

Use a separate Python environment and install dependencies from the repository requirements files. The documentation environment uses Python 3.12; application checks for this documentation update use Python 3.14 on Windows. These are separate environments. Other operating systems require the native libraries used by Qt, and are not certified by this Windows check.

The dependency declarations require NumPy, SciPy, Matplotlib, and PyQt5. `requirements-endf.txt` additionally installs the `endf` reader. Use that file for evaluated ENDF data.

## Windows / PowerShell

Install Python and Git, then run:

```powershell
git clone https://github.com/rspassyuk/KazNRDC.git NuMatRx
cd NuMatRx
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-endf.txt
```

Run the [quick-start calculation](quickstart.md) before installing any external databases:

```powershell
.\.venv\Scripts\python.exe examples/documentation_quickstart.py
```

After [setting up nuclear data](nuclear-data.md), launch the desktop application from the repository root:

```powershell
.\.venv\Scripts\python.exe model/core.py
```

These commands call the environment's interpreter directly; PowerShell script activation is unnecessary. The repository URL retains its historical name, while the application is named NuMatRx.

## Linux and macOS

Use the same repository and a virtual environment:

```bash
git clone https://github.com/rspassyuk/KazNRDC.git NuMatRx
cd NuMatRx
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-endf.txt
.venv/bin/python examples/documentation_quickstart.py
.venv/bin/python model/core.py
```

The final command requires a graphical desktop and compatible Qt platform libraries. The desktop workflow has not been verified on every platform. A missing Qt platform plugin is an environment issue; inspect its error before changing calculation settings.

## Existing installation

Save sessions and record the current code revision before updating. Check `git status` before pulling changes into a modified working tree. Keep nuclear libraries and private overrides backed up separately. Updating the source does not recalculate saved results; restart the program and rerun Evolution when comparing solver revisions.

This guide installs from source. It does not assume that a maintained installer or a package named `numatrx` exists on PyPI.
