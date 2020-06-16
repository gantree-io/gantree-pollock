#!/usr/bin/env python -e

"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

import setuptools  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path

__package_name__ = "pollock"
repo_user = "flex-dapps"

readme_filename = "README.md"
readme_encoding = "utf-8"
long_description_content_type = "text/markdown"

here = path.abspath(path.dirname(__file__))
with open(path.join(here, readme_filename), encoding=readme_encoding) as f:
    long_description = (
        f.read()
    )  # Get the long description from the README file
with open(
    path.join(here, "{}/version.txt".format(__package_name__)), "r"
) as f:
    version = f.readline().splitlines()[0]

setuptools.setup(
    name=__package_name__,  # Required
    version=version,  # Required
    packages=setuptools.find_packages(),  # Required
    url="https://github.com/{}/{}".format(repo_user,__package_name__),  # required
    setup_requires=["wheel", "setuptools"],
    requires_python=[">=3.7"],  # required python version
    long_description=long_description,  # Optional
    long_description_content_type=long_description_content_type,  # Optional
    package_data={__package_name__: ["version.txt"]},  # Optional
    entry_points={  # Optional
        "console_scripts": [
            "{}={}:__main__.main".format(__package_name__, __package_name__)
        ]
    },
)
