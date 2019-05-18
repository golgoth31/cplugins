import os
from setuptools import find_packages, setup

exec_dir = os.path.dirname(os.path.relpath(__file__))

setup(
    name='cplugins',
    version='0.0.1',
    description='Dev framework for nagios plugins writen in python',
    author='David Sabatie',
    author_email='david.sabatie@notrenet.com',
    url='https://github.com/golgoth31/cplugins',
    packages=find_packages(),
    package_data={'': ['../version.txt']},
    install_requires=['argparse', 'boto3', 'requests', 'urllib3', 'pyopenssl'],
    extras_require={},
    entry_points='''
    '''
)
