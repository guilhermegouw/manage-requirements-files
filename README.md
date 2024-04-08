# Manage Requirements Files

`manage-requirements-files` is a Python CLI tool designed to help developers efficiently manage their project dependencies. It automates the updating of `requirements.txt` and `requirements-dev.txt` by appending new dependencies from the activated Python environment.

## Features

- Detects newly installed packages not listed in `requirements.txt` or `requirements-dev.txt`.
- Appends new dependencies to the appropriate requirements file without duplicating entries.
- Creates `requirements.txt` or `requirements-dev.txt` if they don't already exist.

## Installation

Install `manage-requirements-files` globally using pip:

```sh
pip install manage-requirements-files
````

## Usage

Ensure you activate your project's virtual environment before using the commands:

```sh
source /path/to/your/venv/bin/activate  # for Unix-like systems
\path\to\your\venv\Scripts\activate     # for Windows
```

### Updating Production Dependencies
After installing your production dependencies with pip install, update requirements.txt by running:

```sh
manage-dependencies prod
````
This populates requirements.txt with all recently installed production dependencies.

### Updating Development Dependencies
Following the installation of development dependencies, update requirements-dev.txt by running:
```sh
manage-dependencies dev
```

#### Note
Install dependencies incrementally and categorize them as production or development before running the respective command. Attempting to separate a mixed set of installed dependencies may not yield the desired results.

## How It Works

When manage-dependencies is executed, it:

1. Runs `pip freeze` to list the currently installed packages.
2. Read the existing entries from both `requirements.txt` and `requirements-dev.txt`.
3. Identify any new dependencies that are not listed in either file.
4. Appends these new dependencies to the appropriate file based on the selected mode.

## Global Installation and Environment-Specific Usage

Install `manage-requirements-files` once on your system to use across all Python projects. The tool will adjust `requirements.txt` or `requirements-dev.txt` in the current active virtual environment, allowing you to manage dependencies without needing to install the tool in each environment.

## Contributing

Contributions are welcome! If you would like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature.
3. Add your changes.
4. Submit a pull request.

Please make sure to update tests as appropriate.

## License

Distributed under the MIT License. See LICENSE for more information.

## Contact

Guilherme Gouw - guilherme.gouw@gmail.com
