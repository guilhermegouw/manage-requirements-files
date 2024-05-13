#!/usr/bin/env python
import argparse
import subprocess
import sys
import os


def main():
    parser = argparse.ArgumentParser(description="Manage Python project dependencies.")
    parser.add_argument(
        "mode",
        choices=["prod", "dev"],
        help="Update production or development dependencies.",
    )

    args = parser.parse_args()

    if args.mode == "prod":
        update_requirements("requirements.txt", "requirements-dev.txt")
    else:  # dev
        update_requirements("requirements-dev.txt", "requirements.txt")


def pip_freeze():
    """Get the output of pip freeze as a set of package=version strings."""
    venv_path = os.environ.get("VIRTUAL_ENV")
    if not venv_path:
        print("No active virtual environment found.\nDid you forget to activate it?")
        sys.exit(1)

    pip_path = os.path.join(venv_path, "bin", "pip")

    try:
        output = subprocess.check_output([pip_path, "freeze"], text=True)
        return set(output.splitlines())
    except subprocess.CalledProcessError as e:
        print("An error occurred while running pip freeze: ", e)
        return set()


def read_requirements(filename):
    """Read a requirements file and return its contents as a set,\
        automatically create if not exist."""
    try:
        with open(filename, "r") as file:
            return set(line.strip() for line in file if line.strip())
    except FileNotFoundError:
        open(filename, "a").close()  # Create the file if it does not exist
        return set()


def write_requirements(filename, new_lines):
    """Append new lines to a requirements file."""
    with open(filename, "a") as file:
        for line in new_lines:
            file.write(f"{line}\n")


def update_requirements(target_file, other_file):
    """Update the target requirements file with new dependencies,\
        automatically creating files if they don't exist."""
    current_packages = pip_freeze()
    existing_deps = read_requirements(target_file) | read_requirements(other_file)

    new_dependencies = current_packages - existing_deps

    if new_dependencies:
        write_requirements(target_file, new_dependencies)
        print(f"Updated {target_file} with new dependencies: {new_dependencies}")
    else:
        print(f"No new dependencies to add to {target_file}.")


if __name__ == "__main__":
    main()
