#!/usr/bin/env python
"""
Package installer for the zenoss-hipchat command
"""

from setuptools import setup, find_packages


VERSION = __import__('zenoss_hipchat').VERSION

with open('README.rst') as readme:
    README = readme.read()

setup(
    name='zenoss-hipchat',
    version=VERSION,
    packages=find_packages(),
    package_data={},
    license='GPLv3',
    author='Carson Gee',
    author_email='x@carsongee.com',
    url="http://github.com/carsongee/zenoss-hipchat",
    description=("Command suitable in use for Zenoss notification commands "
                 "for sending events to hipchat."),
    long_description=README,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Information Technology',
        ('License :: OSI Approved :: '
         'GNU Lesser General Public License v3 (LGPLv3)'),
        'Operating System :: POSIX :: Linux',
    ],
    install_requires=[
        'requests',
        ],
    entry_points={'console_scripts': [
        'zenoss-hipchat = zenoss_hipchat.command:entry_point',
    ]},
    zip_safe=True,
)
