# Installation

NuMatRx can be installed **using the installer** or **from source**.
Choose either method below.

## Option 1: Install using the installer

Download the installation file, run it, and follow the setup instructions.

```{admonition} Download NuMatRx and nuclear data
:class: important

**[Download the installer and xsdir nuclear-data libraries](https://drive.google.com/drive/folders/1Qvy23GtS8aMXxuuQK3cA7DE3uszLhbq4?usp=drive_link)**

Download both the **installer** and the **xsdir** archive.
The desktop application needs `xsdir` to load nuclear data and perform calculations.
```

Extract the nuclear-data archive and place the `xsdir` folder in the
application directory. Avoid an extra directory level such as
`xsdir/xsdir`. See {doc}`nuclear-data` for the required structure
and configuration.

Once the data are configured, launch the installed application.

## Option 2: Install from source

You need **Python 3.11 or newer** and **Git**.
The application uses NumPy, SciPy, Matplotlib and PyQt5;
the optional `endf` package reads ENDF-6 files.

::::{tab-set}

:::{tab-item} Windows (PowerShell)
```powershell
git clone https://github.com/rspassyuk/NuMatRx.git NuMatRx
cd NuMatRx
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-endf.txt
```
:::

:::{tab-item} Linux / macOS
```bash
git clone https://github.com/rspassyuk/NuMatRx.git NuMatRx
cd NuMatRx
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-endf.txt
```

On Linux, Qt also needs system libraries for its display backend.
If the application reports an error about the *xcb* platform plugin,
install your distribution's required Qt runtime packages.
:::
::::

There are two requirements files:

| File | Installs | Use it when |
|---|---|---|
| `requirements-endf.txt` | NumPy, SciPy, Matplotlib, PyQt5 and the `endf` reader | You work with ENDF-6 libraries (recommended). |
| `requirements.txt` | NumPy, SciPy, Matplotlib and PyQt5 | You only need MACS tables, TALYS or your own data. |

```{important}
The GitHub repository does not include the nuclear-data libraries.
For desktop calculations, download and extract **xsdir** from the
[downloads folder](https://drive.google.com/drive/folders/1Qvy23GtS8aMXxuuQK3cA7DE3uszLhbq4?usp=drive_link).
Place it in the repository root, alongside `core`, `model`, and
`nuclear_data`, then follow {doc}`nuclear-data`.
```

### Installation check (source installation)

Run the built-in test calculation. This synthetic example does not
need `xsdir` or any other nuclear data:

::::{tab-set}
:::{tab-item} Windows
```powershell
.\.venv\Scripts\python.exe examples/documentation_quickstart.py
```
:::
:::{tab-item} Linux / macOS
```bash
.venv/bin/python examples/documentation_quickstart.py
```
:::
::::

The script prints `"passed": true` when its solver and averaging
checks pass. The {doc}`first-calculation` page explains the synthetic test. Continue with {doc}`first-gui-run` for a Pb–Bi–Po calculation through Python or the GUI.

### Start from source

After configuring `xsdir`, run the following command from the
repository folder:

::::{tab-set}
:::{tab-item} Windows
```powershell
.\.venv\Scripts\python.exe model/core.py
```
:::
:::{tab-item} Linux / macOS
```bash
.venv/bin/python model/core.py
```
:::
::::

A splash screen shows the data being loaded. When loading finishes,
the main window opens on the *Periodic Table* workspace.

```{tip}
You do not need to activate the virtual environment:
calling its Python executable directly is enough.
```

### Update a source installation

From the repository folder:

::::{tab-set}
:::{tab-item} Windows
```powershell
git pull --ff-only
.\.venv\Scripts\python.exe -m pip install -r requirements-endf.txt
```
:::
:::{tab-item} Linux / macOS
```bash
git pull --ff-only
.venv/bin/python -m pip install -r requirements-endf.txt
```
:::
::::

Restart the application after updating. Saved sessions retain
previously calculated results; rerun a calculation to obtain results
with the updated version.
