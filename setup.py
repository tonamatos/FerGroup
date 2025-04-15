# setup.py

from setuptools import setup, find_packages

setup(
  name="FerGroup",
  version="1.0.0",
  description="The comprehensive framework for the study of Amoeba graphs and the Fer group",
  author="Tonatiuh Matos-Wiederhold",
  packages=find_packages(),
  include_package_data=True,
  python_requires='>=3.7',
  install_requires=[
    'networkx',
    'sympy'
  ],
)
