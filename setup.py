# Copyright 2015 University of Edinburgh
# Licensed under GPLv3 - see README.md for information

from setuptools import setup, find_packages

setup(
    name='read-device',
    version='3.1.8',
    description='Collect metrics from real-world devices',
    url='https://github.com/lewiseason/read-device',
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Environment :: Console',
      'Intended Audience :: Developers',
      'Intended Audience :: System Administrators',
      'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
      'Natural Language :: English',
      'Programming Language :: Python :: 2.7',
      'Programming Language :: Python :: 3',
      'Topic :: System :: Monitoring',
    ],
    author='Lewis Eason',
    author_email='me@lewiseason.co.uk',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'lxml',
        'texttable',
        'requests',
        'peewee',
    ],
    entry_points='''
        [console_scripts]
        device=read_device.commands.device:main
        meters=read_device.commands.meters:main
    '''
)
