# Installation Guide

There are a few steps you will need to complete before being able to run `rain` for yourself.
The first one of these is to install the `rain` software package.
There are two ways of doing this:

- Installing directly from PyPI
- Installing from the GitHub repository

This guide will show the necessary steps for both options.

## Setting up a virtual environment

Virtual environments allow you to install and run Python software while keeping it fenced away from the rest of your system.
Running a software package from its own dedicated virtual environment means you can install only the dependencies a particular package requires.
If a software package is only stored in a virtual environment, then uninstalling it is a simple process (deleting the virtual environment folder does the trick) and does not affect the rest of your system.
Virtual environments also have Python and some tools (such as 'pip') installed by default.
For these reasons it is highly recommended to install and run `rain` from a virtual environment.
More information about virtual environments can be found in the [Python documentation](https://docs.python.org/3/library/venv.html)

If you would like to create a virtual environment to install `rain` into, you will need to open a command line terminal such as PowerShell on Windows or Fish or zsh on Linux.
In this terminal you will need to enter the following command:
```
python -m venv path/to/folder
```

If you want to create the virtual environment in the folder you are currently in, you can use the following:

- On a Windows system: `python -m venv folder`
- On a Linux system: `python -m venv ./folder`

The command can take a few seconds to complete.

This will create a folder in the location you gave, called "folder", containing your virtual environment.
With the virtual environment created, you can now start it by entering the following command:
```
source folder/bin/activate
```
You are now ready to install `rain`!

## Option 1: Installing from PyPI

PyPI is a repository containing all of the Python packages that can be installed using 'pip'.
This makes it very easy to install packages that have reached a certain degree of maturity.
You can read more about PyPI [here](https://pypi.org/).

You can install `rain` by entering the following command with your virtual environment activated:
```
pip install rain
```

This instructs pip to install `rain` and its external dependencies within the virtual environment you have activated.

## Option 2: Installing from GitHub

You can also install `rain` directly from the public GitHub repository, by entering the following commands with your virtual environment activated:
```
git clone https://github.com/danielk333/rain
pip install .
```
The first command clones the online repository into the folder you are currently in, and the second command instructs pip to install what you have just cloned.
