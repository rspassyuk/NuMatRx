# Installation

NuMatRx can be installed using the downloadable installer or run from
Python source.

## Option 1: Use the installer

Download the installer from the
[NuMatRx downloads folder](https://drive.google.com/drive/folders/1Qvy23GtS8aMXxuuQK3cA7DE3uszLhbq4?usp=drive_link),
run it, and follow the installation instructions.

Nuclear-data files are distributed separately through the same folder.
Download and extract the required datasets, then follow
{doc}`nuclear-data` to configure their location before starting a calculation.

```{note}
The Python and Git instructions below apply to installation from source.
```

## Option 2: Install from source

You need **Python 3.11 or newer** and **Git**.
The application uses NumPy, SciPy, Matplotlib and PyQt5;
the optional `endf` package reads ENDF-6 files.
