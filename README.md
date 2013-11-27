AWSTools
========

Python-based tools for AWS, using boto or AWS shell commands.

Example:

    ec2sh (ec2-machine-name)

Opens up a terminal on an EC2 machine by machine name so that you don't have to know the dynamic hostname.


To Build:
---------

    $ python setup.py sdist --formats gztar

To Install:
-----------

You need Python 2.7 or above with PIP installed.  Here are the most reliable instructions I've seen:
http://www.pip-installer.org/en/latest/installing.html

Check the version number.  This argument can be either a relative file path or URL.

    $ sudo pip install dist/G11AWSTools-0.1.1.tar.gz
