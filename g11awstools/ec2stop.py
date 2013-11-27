__author__ = 'Andy Jenkins'
import logging
import sys
import os
import argparse
import ec2 as EC2
from BaseTool import BaseTool
LOG = logging.getLogger("ec2stop")


class ec2stop(BaseTool):

    def run(self, parser):
        """Shuts down an EC2 instance by name"""
        parser.add_argument("instance_name", help="The friendly name of the EC2 image you want to connect to")
        args = self.parse_args()

        ec2 = EC2.ec2()

        # Ensure we have exactly 1 instance with the desired name
        instance = ec2.instances().get("Name", args.instance_name)
        if not instance:
            raise Exception("No instance found for name %s" % args.instance_name)
        elif len(instance) > 1:
            raise Exception("Found multiple instances for %s: %s", args.instance_name, instance)
        instance = instance[0]

        cur_state = instance["State"]["Name"]
        if  cur_state == "stopped":
            raise Exception("Instance %s is already stopped", args.instance_name)

        LOG.info("Instance %s is %s. Stopping now", args.instance_name, cur_state)

        # Ensure the instance is started, or start if requested
        ec2.stop_instance(instance)

if __name__ == '__main__':
   ec2stop().main()


