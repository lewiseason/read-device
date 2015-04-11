from setuptools import setup, find_packages

setup(
    name='read-device',
    version='3.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'lxml',
        'texttable',
    ],
    entry_points='''
        [console_scripts]
        device=read_device.command_line:main
    '''
)
