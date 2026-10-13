# Installation

NuMatRx runs from source. You need **Python 3.11 or newer** and **Git**. The application uses NumPy, SciPy, Matplotlib and PyQt5; the optional `endf` package reads ENDF-6 files.

## Install

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
On Linux, Qt also needs the usual X11/Wayland system libraries. If the application fails with a message about the *xcb* platform plugin, install your distribution's Qt runtime packages.
:::
::::

There are two requirement files:

| File | Installs | Use it when |
|---|---|---|
| `requirements-endf.txt` | everything below **plus** the `endf` reader | you work with ENDF-6 libraries (recommended) |
| `requirements.txt` | NumPy, SciPy, Matplotlib, PyQt5 | you only need MACS tables, TALYS or your own data |

## Check the installation

Run the built-in test calculation. It does not need any nuclear data:

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

The script prints `"passed": true` when all four solvers reproduce the exact solution. {doc}`first-calculation` explains what it computes.

## Start the application

The desktop application needs nuclear data, so first follow {doc}`nuclear-data`. Then, from the repository folder:

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

A splash screen shows the data being loaded. When it closes, the main window opens on the *Periodic Table* workspace.

```{tip}
You do not need to activate the virtual environment: calling `.venv` Python directly is enough.
```

## Update

```bash
git pull
.venv/bin/python -m pip install -r requirements-endf.txt
```

Restart the application after updating. Saved sessions keep the results they were saved with; rerun a calculation if you want it computed by the new version.
I also need to say that there is an installation file and you can get started like this, which is located at the link:
https://drive.google.com/drive/folders/1Qvy23GtS8aMXxuuQK3cA7DE3uszLhbq4?usp=drive_link
