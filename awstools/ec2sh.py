__author__ = 'gear11.com'
from subprocess import Popen, PIPE, STDOUT
import logging
import json
import sys
import itertools

from optparse import OptionParser

LOG = logging.getLogger("ec2sh")

def ec2_instances():
    """Returns a list of dictionaries containing metadata for EC2 instances.
     The attributes are derived from the <tt>aws ec2 describe-instances</tt> command."""
    cmd = 'aws ec2 describe-instances'
    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    s = p.stdout.read()
    LOG.debug(s)
    rsp = json.loads(s)
    for i in itertools.chain([r["Instances"][0] for r in rsp["Reservations"]]):
        print "Name: %s, ID: %s, DNS: %s" % (i["Tags"][0]["Value"], i["InstanceId"], i["PublicDnsName"])

def main():
    logging.basicConfig(format = '%(asctime)-15s %(levelname)s:%(name)s:%(message)s', level=logging.INFO, stream = sys.stderr)
    parser = OptionParser()
    (options, args) = parser.parse_args()
    target = args[0]


if __name__ == '__main__':
   main()


