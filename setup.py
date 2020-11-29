#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import re
import sys
from shutil import rmtree

from setuptools import Command, find_packages, setup


URL = "https://github.com/mondeja/http-request-codegen"
EMAIL = "mondejar1994@gmail.com"
AUTHOR = "Álvaro Mondéjar Rubio"

REQUIRES_PYTHON = ">=3"
REQUIRED = [
    'faker>=4.0.0',  # Python3 only support
]
LINT_EXTRAS = [
    "flake8==3.8.4",
    "flake8-print==4.0.0",
    "flake8-implicit-str-concat==0.2.0",
    "isort==5.6.4",
    "yamllint==1.25.0",
]
TEST_EXTRAS = [
    "pytest==6.1.2",
    "pytest-cov==2.10.1",
    "tox==3.20.1",
]
DOC_EXTRAS = [
    "mkdocs==1.1.2",
    "mkdocs-material==6.1.6",
    "mkdocs_macros_plugin==0.5.0",
    "mkdocs-minify-plugin==0.3.0",
]
DEV_EXTRAS = [
    "twine==3.2.0",
    "bump2version==1.0.1",
    "pre-commit==2.9.2",
] + DOC_EXTRAS + TEST_EXTRAS + LINT_EXTRAS

HERE = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(HERE, "README.md"), encoding="utf-8") as f:
    LONG_DESCRIPTION = "\n" + f.read()

ABOUT = {}
INIT_FILEPATH = os.path.join(HERE, "http_request_codegen", "__init__.py")
with io.open(INIT_FILEPATH, encoding="utf-8") as f:
    content = f.read()
    ABOUT["__title__"] = \
        re.search(r"__title__\s=\s[\"']([^\"']+)[\"']", content).group(1)
    ABOUT["__version__"] = \
        re.search(r"__version__\s=\s[\"']([^\"']+)[\"']", content).group(1)
    ABOUT["__description__"] = \
        re.search(r"__description__\s=\s[\"']([^\"']+)[\"']", content).group(1)


class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = [
        ("test", None, "Specify if you want to test your upload to Pypi."),
    ]

    @staticmethod
    def status(s):
        """Prints things in bold."""
        sys.stdout.write("\033[1m{0}\033[0m\n".format(s))

    def initialize_options(self):
        self.test = None

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(HERE, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system("{0} setup.py sdist bdist_wheel --universal".format(
            sys.executable))

        self.status("Uploading the package to PyPI via Twine…")
        cmd = "twine upload%s dist/*" % (
            " --repository-url https://test.pypi.org/legacy/" if self.test
            else ""
        )
        os.system(cmd)
        sys.exit()


setup(
    name=ABOUT["__title__"],
    version=ABOUT["__version__"],
    description=ABOUT["__description__"],
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=["tests"]),
    install_requires=REQUIRED,
    extras_require={
        "dev": DEV_EXTRAS,
        "test": TEST_EXTRAS,
        "lint": LINT_EXTRAS,
        "doc": DOC_EXTRAS,
    },
    include_package_data=True,
    license="BSD License",
    classifiers=[
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Documentation",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    cmdclass={
        "upload": UploadCommand,
    },
)
