from setuptools import find_packages
from setuptools import setup

setup(
    name='sr_interfaces',
    version='1.0.0',
    packages=find_packages(
        include=('sr_interfaces', 'sr_interfaces.*')),
)
