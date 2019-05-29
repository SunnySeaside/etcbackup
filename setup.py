#!/usr/bin/env python
from setuptools import setup, find_packages
setup(
    name="etcbackup",
    version="0.1",
    packages=find_packages(),
    install_requires=["appdirs","pyyaml","borgbackup"],
    extras_require={"archlinux":["pyalpm"]},
    entry_points={
        'console_scripts':["etcbackup = etcbackup.main:main"]
        #todo use entry points for plugins?
    }
)
