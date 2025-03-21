[![python](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
![os](https://img.shields.io/badge/os-ubuntu%20|%20macos%20|%20windows-blue.svg)
[![license](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/sandialabs/sibl#license)

[![codecov](https://codecov.io/gh/mlanduyt/Assignment1/graph/badge.svg?token=V8BG4FHMD7)](https://codecov.io/gh/mlanduyt/Assignment1)
[![tests](https://github.com/mlanduyt/Assignment1/actions/workflows/tests.yml/badge.svg)](https://github.com/mlanduyt/Assignment1/actions)


### Getting Started

### Conda environment, install, and testing <a name="install"></a>

To install this package, please begin by setting up a conda environment (mamba also works):
```bash
conda create --name bisection-method-env python=3.12
```
Once the environment has been created, activate it:

```bash
conda activate bisection-method-env
```
Double check that python is version 3.12 in the environment:
```bash
python --version
```
Ensure that pip is using the most up to date version of setuptools:
```bash
pip install --upgrade pip setuptools wheel
```
Create an editable install of the bisection method code (note: you must be in the correct directory):
```bash
pip install -e .
```