__author__ = 'Andy Jenkins'
import logging
import sys
import os
import argparse
from ec2 import ec2
from BaseTool import BaseTool
LOG = logging.getLogger("ec2sh")


class ec2sh(ec2):

    def run(self, parser):
        """Allows you to SSH into an EC2 instance by the friendly "Name" tag rather than the IP.  As in:
            ec2sh WebServer1
        Takes as input your SSH key PEM file, and the friendly name of the server you want to connect to."""
        parser.add_argument("instance_name", help="The friendly name of the EC2 image you want to connect to")
        parser.add_argument("-k", "--key",
                            help="Path to your EC2 instance key (will be read from EC2_SSH_KEY env var if not provided)")
        parser.add_argument("-u", "--username",
                            help="Username to use, defaults to ec2-user", default="ec2-user")
        parser.add_argument("-s", "--start", help="Start the instance if not yet started.", action='store_true')
        args = self.parse_args(parser)

        ssh_key = args.key if args.key else os.getenv("EC2_SSH_KEY")
        if not ssh_key:
            raise Exception("SSH Key must be specified via EC2_SSH_KEY env var or --key option")
        else:
            LOG.info("Using SSH Key %s" % ssh_key)

        # Ensure we have exactly 1 instance with the desired name
        instance = self.instances().find("Name", args.instance_name)
        if not instance:
            raise Exception("No EC2 instance found for name %s" % args.instance_name)
        elif len(instance) > 1:
            raise Exception("Found multiple EC2 instances for %s: %s", args.instance_name, instance)
        instance = instance[0]

        # Ensure the instance is started, or start if requested
        dns_name = instance["PublicDnsName"]
        if not dns_name:
            if not instance["State"]["Name"] == "stopped":
                raise Exception("Instance %s has no DNS name but its state is not stopped. Re-check JSON")
            if not args.start:
                raise Exception("Instance %s is not started. Invoke with -s option to start." % args.instance_name)
            else:
                instance = self.start_instance(instance, True)
                dns_name = instance["PublicDnsName"]

        # SSH into the instance
        cmd_args = ['ssh', '-i', ssh_key, '%s@%s' % (args.username, dns_name) ]
        LOG.info("Executing '%s'", ' '.join(cmd_args))
        os.execvp(cmd_args[0], cmd_args)

def main():
    ec2sh().main()

if __name__ == '__main__':
   main()


