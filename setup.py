"""Setup.py loop."""
from setuptools import find_packages, setup

setup(
    name="src",
    version="0.0.1",
    author="Simon Thomas",
    author_email="sdat2@cam.ac.uk",
    description="Full scripts to generate figures for 'Defining Southern"
                 + "Ocean fronts using unsupervised classification'",    
    url="https://github.com/so-wise/so-fronts",
    packages=find_packages(),
    test_suite="src.tests.test_all.suite",
)
