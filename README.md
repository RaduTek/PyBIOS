# PyBIOS

A BIOS simulator that runs in the terminal, written in Python.

## Why

Just for fun :)

## Dependencies

-   Python 3 (I have developed it on Python 3.12, so it's not guaranteed to work properly on older versions)
-   UNIX/Posix compliant system and a VT100 terminal emulator

## How to run

For now, run `ami_test.py` to get a simulation of AMI BIOS.

## Features

-   Graphics routines for drawing boxes and filling areas with colors
-   Color palette structures
-   Message boxes and selection dialogs
-   BIOS menus are defined as dictionaries
    -   Menu items can have a select function or predefined editable types
