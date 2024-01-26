# neaspec SDK Documentation
Contains examples and other documentation for neaspec SDK. There are
 1. Examples based on `nea_tools` which is a pure Python wrapper for the SDK for usage with stand-alone scripts.
 2. Examples without `nea_tools` for usage in neaSCAN console.
 3. Storyboards for creating custom scanning behaviors (scan route and signal processing) in form of `JSON` files.
 4. Application of common use cases of the SDK.
 5. Usage of `neagui`.

## Storyboards

Storyboard scans are `JSON` files which provide parameters and executable code to the server. This code is written in `ExprTk` https://github.com/ArashPartow/exprtk.
In contrast to standard `JSON`, these files may contain comments in C-like style (`/* .. */` or `// ...`) on any level. Correct handling of such comments require neaSCAN version ≥ 2.1.10752.
Such comments are displayed as errors by github code preview.

Paste any storyboard to http://nea-server/storyboard/edit/by-name/new (only accessible from client PC). See http://nea-server/storyboard for further documentation.

## nea_tools

`nea_tools` is a pure Python wrapper which is built on top of the standard neaspec SDK. It aims to facilitate the usage of the SDK by converting to standard Python objects like `numpy` arrays, allows type hinting and linting.

## neagui

`neagui` is Python package for an alternative GUI to control and monitor a neaSCOPE. It is based on `PySide`, `pyqtgraph` and `nea_tools` and is designed to be easily extendable while also providing simple access to most core functionalities to handle a neaSCOPE. The default usage of `neagui` is the ExpertMode which includes all major widgets i.e. expertmode.exe is installed alongside the installation of neagui. Yet, it can be used as standard Python package to import and use individual widgets.


