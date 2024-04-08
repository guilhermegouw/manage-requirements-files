from setuptools import setup, find_packages

setup(
    name="manage_requirements_files",
    version="0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "manage-dependencies=manage_requirements_files.cli:main",
        ],
    },
    author="Guilherme Gouw",
    author_email="guilherme.gouw@gmail.com",
    description="A utility to manage project dependencies for development and production.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/guilhermegouw/manage-requirements-files",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
