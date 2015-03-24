from setuptools import setup

setup(
    name='Read Device',
    version='3.0',
    py_modules=['command_line'],
    install_requires=[
        'Click',
        'lxml',
        'texttable',
    ],
    entry_points='''
        [console_scripts]
        device=command_line:main
    '''
)
