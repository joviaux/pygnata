## Pygnata
[![Build Status](https://scrutinizer-ci.com/g/joviaux/pygnata/badges/build.png?b=master)](https://scrutinizer-ci.com/g/joviaux/pygnata/build-status/master)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/joviaux/pygnata/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/joviaux/pygnata/?branch=master)
[![PyPI version](https://badge.fury.io/py/pygnata.svg)](http://badge.fury.io/py/pygnata)
#### Description
Pygnata is a command-line application for creating a project tree from a template file (.pyg file).
#### Features
 * Create a project tree from a .pyg file.
 * Generate a .pyg file from an existing path.
 * Use YAML and Jinja2 for the template file.

#### Setup 
To install Pygnata, just clone the repository and make a python setup:
```bash
git clone https://github.com/joviaux/pygnata.git
cd pygnata
python setup.py install
```

or with **pip**:

```bash
pip install pygnata
```
#### Usage
##### Create project tree from a .pyg file
```bash
pygnata <my_pyg_file_name>
```
##### Create a .pyg file from a existing path
```bash
pygnata create [options] <source_path> <destination_pyg_file_path>
```
##### Show the content of a .pyg file
```bash
pygnata show <my_pyg_file_name>
```
##### Save a .pyg file in the ~/.pygnata folder
```bash
pygnata save <source_pyg_file_path>
```

##### 

#### Examples

##### The .pyg file

##### Pre-defined templates

You can find pre-defined templates at https://github.com/joviaux/pygnata-templates
Feel free to contribute!
