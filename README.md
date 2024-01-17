# txt2sduml

**THIS DOCUMENT IS AI TRANSLATED.**
original: [ja](README.ja.md)

Generate sequence diagram images from text files written in the format of sequencediagram.org.

## Requirements

- Python (>=3.8)
- pip (>=21)

## Dependencies

- Playwright

## How it Works

It opens sequencediagram.org in a headless browser, pastes the source code from the specified file into the editor, and then downloads the sequence diagram in SVG format.

## Installation

Download from [releases](../../releases/latest) and install using the following command:

```shell
$ pip install txt2sduml-0.1.0-py3-none-any.whl
```

For the first installation, Playwright needs to be installed.

The playwright command is installed during the resolution of txt2sduml dependencies, but in some cases, if the PATH is not set, the installed playwright and txt2sduml may not be found.

```shell
$ playwright install
```

## Upgrade

Download the new package from releases and upgrade using the following command:

```shell
$ pip install --upgrade txt2sduml-0.1.0-py3-none-any.whl
```
