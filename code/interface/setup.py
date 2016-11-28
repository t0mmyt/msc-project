#!/usr/bin/env python3
from distutils.core import setup
import os

datadirs = ['templates', 'static']
datafiles = []
for datadir in datadirs:
    datafiles.extend(
        ('interface/{}'.format(datadir), [os.path.join(d, f) for f in files])
        for d, folders, files in os.walk(datadir)
    )

setup(
    name='interface',
    version='0.0.1',
    description='Web interface',
    author='Tom Taylor',
    author_email='tom@tommyt.co.uk',
    url='https://github.com/t0mmyt/msc-project/code/observation',
    packages=['interface'],
    data_files=datafiles
)
