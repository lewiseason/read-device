from setuptools import setup, find_packages

setup(
    name='read-device',
    version='3.1.3',
    description='Collect metrics from real-world devices',
    #url=''
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Programming Language :: Python :: 2.7',
      'Programming Language :: Python :: 3',

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
