"""

To create python eggs distribution run:

    $python setup.py bdist_egg

Egg is supported package option in azure databricks
"""
from setuptools import setup, find_packages

setup(
    name="bokeh_templates",
    version="0.1",
    packages=find_packages()
)
