__author__ = 'Andy Jenkins'
import logging
from ec2 import ec2
import time

LOG = logging.getLogger("ec2stop")


class ec2stop(ec2):

    def run(self, parser):
        """Shuts down an EC2 instance by name"""
        parser.add_argument("instance_name", help="The friendly name of the EC2 image you want to connect to")
        parser.add_argument("-x", "--block", help="Block until the stop operation is confirmed", action='store_true')
        args = self.parse_args(parser)

        # Ensure we have exactly 1 instance with the desired name
        instance = self.instances().find("Name", args.instance_name)
        if not instance:
            raise Exception("No instance found for name %s" % args.instance_name)
        elif len(instance) > 1:
            raise Exception("Found multiple instances for %s: %s", args.instance_name, instance)
        instance = instance[0]
        cur_state = instance["State"]["Name"]
        if cur_state == "stopped":
            print("Instance %s is already stopped" % args.instance_name)
        else:
            LOG.info("Instance %s is %s. Stopping now", args.instance_name, cur_state)
            instance = self.stop_instance(instance, args.block)
            if args.block:
                print "Stopped EC2 instance %s" % instance["Name"]
            else:
                print "Issued stop command for EC2 instance %s" % instance["Name"]


def main():
    ec2stop().main()

if __name__ == '__main__':
    main()