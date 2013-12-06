from __future__ import with_statement

__author__ = 'Andy Jenkins'

try:
   from setuptools import setup
   extra = dict(include_package_data=True)
except ImportError:
   from distutils.core import setup
   extra = {}

setup(
    name='G11AWSTools',
    version='0.1.1',
    author=__author__,
    author_email='andy@gear11.com',
    packages=['g11awstools', 'g11pyutils'],
    url='https://github.com/gear11/G11AWSTools',
    license='GPLv3',
    description='Tools for AWS, built on AWS CLI',
    long_description=open('README.md').read(),
    install_requires=[
    ],
      entry_points = {
        'console_scripts': [
            'ec2 = g11awstools.ec2:main',
        ]},
    **extra
)