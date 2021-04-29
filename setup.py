"""Setup.py loop."""
from setuptools import find_packages, setup

setup(
    name="src",
    version="0.0.1",
    author="Simon D.A. Thomas",
    author_email="sdat2@cam.ac.uk",
    description="Full scripts to generate figures for OS022-08 talk at AGU 2020",
    url="https://github.com/sdat2/sof-agu",
    packages=find_packages(),
    test_suite="src.tests.test_all.suite",
)


# python3 src/data_loading/download.py
