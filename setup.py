from __future__ import with_statement

__author__ = 'Andy Jenkins'

try:
   from setuptools import setup
   extra = dict(include_package_data=True)
except ImportError:
   from distutils.core import setup
   extra = {}

def readme():
   with open("README.md") as f:
      return f.read()

setup(
    name='G11AWSTools',
    version='0.1.1',
    author=__author__,
    #author_email='',
    packages=['g11awstools', 'g11pyutils'],
    url='https://github.com/gear11/G11AWSTools',
    license='GPLv3',
    description='Tools for AWS, built on AWS CLI',
    long_description=readme(),
    install_requires=[
    ],
      entry_points = {
        'console_scripts': [
            'ec2sh = g11awstools.ec2sh:main',
        ]},
    **extra
)