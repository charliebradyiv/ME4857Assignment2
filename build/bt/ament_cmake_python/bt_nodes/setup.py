from setuptools import find_packages
from setuptools import setup

setup(
    name='bt_nodes',
    version='1.0.0',
    packages=find_packages(
        include=('bt_nodes', 'bt_nodes.*')),
)
