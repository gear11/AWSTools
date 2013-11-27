G11AWSTools
===========

Python-based tools for AWS, built on the AWS Command Line Interface

Example:

    ec2sh [-k key] [-s] ec2-machine-name

Opens up a terminal on an EC2 machine by machine name so that you don't have to know the dynamic hostname.  Starts
the machine if not yet started.


To Build:
---------

    $ python setup.py sdist --formats gztar

To Install:
-----------
The tools are Python wrappers around the AWS Command Line Interface.  To install the AWS CLI, see here:
http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-set-up.html

You need Python 2.7 with PIP installed. Here are the most reliable instructions I've seen:
http://www.pip-installer.org/en/latest/installing.html

Here is the command to install via `pip`.  Make sure the version is aligned with the `tar.gz`. The argument
can be either a relative file path or URL.

    $ sudo pip install dist/G11AWSTools-0.1.1.tar.gz
