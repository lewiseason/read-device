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
        'requests',
    ],
    entry_points='''
        [console_scripts]
        device=read_device.commands.device:main
        meters=read_device.commands.meters:main
    '''
)
#
        # device=read_device.command_line:device.main
        # record=read_device.command_line:record.main
