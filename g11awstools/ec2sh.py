__author__ = 'Andy Jenkins'
from subprocess import Popen, PIPE, STDOUT
import logging
import json
import sys
import itertools
from g11pyutils import IndexedDictList
import os
import argparse
LOG = logging.getLogger("ec2sh")


def main():
    """Allows you to SSH into an EC2 instance by the friendly "Name" tag rather than the IP.  As in:
        ec2sh WebServer1
    Takes as input your SSH key PEM file, and the friendly name of the server you want to connect to."""
    parser = argparse.ArgumentParser()
    parser.add_argument("image_name", help="The friendly name of the EC2 image you want to connect to")
    parser.add_argument("-k", "--key",
                        help="Path to your EC2 instance key (will be read from EC2_SSH_KEY env var if not provided)")
    parser.add_argument("-d", "--debug", help="Print debug info")
    args = parser.parse_args()

    level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(format = '%(asctime)-15s %(levelname)s:%(name)s:%(message)s', level=level, stream = sys.stderr)

    ssh_key = args.key if args.key else os.getenv("EC2_SSH_KEY")
    if not ssh_key:
        raise Exception("SSH Key must be specified via EC2_SSH_KEY env var or --key option")

    instance = ec2_instances().get("Name", args.image_name)
    if not instance:
        raise Exception("No instance found for name %s" % args.image_name)
    elif len(instance) > 1:
        raise Exception("Found multiple instances for %s: %s", args.image_name, instance)

    cmd_args = ['ssh', '-i', ssh_key, 'ubuntu@%s' % instance[0]["PublicDnsName"]]
    LOG.info("Executing '%s'", ' '.join(cmd_args))
    os.execvp(cmd_args[0], cmd_args)


def ec2_instances():
    """Returns a list of dictionaries containing metadata for EC2 instances.
     The attributes are derived from the <tt>aws ec2 describe-instances</tt> command."""
    cmd = 'aws ec2 describe-instances'
    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    s = p.stdout.read()
    LOG.debug(s)
    rsp = json.loads(s)
    instances = []
    for i in itertools.chain([r["Instances"][0] for r in rsp["Reservations"]]):
        # Assign name
        i["Name"] = i["Tags"][0]["Value"]
        instances.append(i)
        LOG.debug("Name: %s, ID: %s, DNS: %s" % (i["Name"], i["InstanceId"], i["PublicDnsName"]))
    return IndexedDictList(instances)


if __name__ == '__main__':
   main()


