#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os.path import dirname, abspath, join

base_path = dirname(abspath(__file__))

with open(join(base_path, "README.md")) as readme_file:
    readme = readme_file.read()

with open(join(base_path, "requirements.txt")) as req_file:
    requirements = req_file.readlines()

setup(
    name="tulpa",
    description='Tulpa - Generate research datasets from videogame metadata',
    long_description=readme,
    license="GPL-3.0",
    author='Diggr Team',
    author_email='team@diggr.link',
    url='https://github.com/diggr/tulpa',
    packages=find_packages(exclude=['dev', 'docs']),
    package_dir={
            'tulpa': 'tulpa'
        },
    version="1.0.0",
    py_modules=["tulpa", "datasets", "visualizations"],
    install_requires=requirements,
    include_package_data=True,
    entry_points="""
        [console_scripts]
        tulpa=tulpa.cli:cli
    """,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: System :: Logging',
    ],
    keywords=[
        'research data', 'data visualization', 'data analysis'
    ],
)
