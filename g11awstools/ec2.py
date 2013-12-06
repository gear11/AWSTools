__author__ = 'jenkins'
import logging
from subprocess import Popen, PIPE, STDOUT
import json
import itertools
from g11pyutils import IndexedDictList, StopWatch
import sys
import argparse
import time


LOG = logging.getLogger("ec2")

class ec2:
    """A base class for EC2 tools, including utility functions, and also a main dispatcher"""
    def parse_args(self, parser):
        args = parser.parse_args()
        level = logging.DEBUG if args.debug else logging.INFO
        logging.basicConfig(format='%(asctime)-15s %(levelname)s:%(name)s:%(message)s', level=level, stream=sys.stderr)
        return args

    def start_instance(self, instance, block):
        """Starts the given EC2 instance, optionally blocking until it completes."""
        LOG.info("Starting EC2 instance %s. Cultivate the virtue of patience." % instance["Name"])
        self.popen_aws("aws ec2 start-instances --instance-ids %s" % instance["InstanceId"])
        if block:
            while instance["State"]["Name"] != "running":
                time.sleep(5.0)
                instance = self.refresh(instance)
            LOG.info("Instance started, allowing 30s for SSH to init")
            time.sleep(30)
        return instance

    def stop_instance(self, instance, block):
        """Starts the given EC2 instance, optionally blocking until it completes."""
        LOG.info("Stopping EC2 instance %s. Cultivate the virtue of patience." % instance["Name"])
        self.popen_aws("aws ec2 stop-instances --instance-ids %s" % instance["InstanceId"])
        if block:
            while instance["State"]["Name"] != "stopped":
                time.sleep(5.0)
                instance = self.refresh(instance)
        return instance

    def instances(self):
        """Returns a list of dictionaries containing metadata for EC2 instances.
         The attributes are derived from the <tt>aws ec2 describe-instances</tt> command."""
        rsp, _ = self.popen_aws("aws ec2 describe-instances")
        instances = []
        for i in itertools.chain([r["Instances"][0] for r in rsp["Reservations"]]):
            # Assign name
            i["Name"] = i["Tags"][0]["Value"]
            instances.append(i)
            LOG.debug("Name: %s, ID: %s, DNS: %s" % (i["Name"], i["InstanceId"], i["PublicDnsName"]))
        return IndexedDictList(instances)

    def refresh(self, instance):
        """Refreshes and returns the AWS data for the given instance"""
        rsp, _ = self.popen_aws("aws ec2 describe-instances --instance-ids %s" % instance["InstanceId"])
        i = rsp["Reservations"][0]["Instances"][0]
        i["Name"] = i["Tags"][0]["Value"]
        return i

    def popen_aws(self, cmd):
        """Executs the AWS command (via Popen) and returns a tuple of (JSON stdout, str stderr)"""
        LOG.debug("Executing AWS cmd \"%s\"", cmd)
        p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        sout = p.stdout.read()
        serr = p.stderr.read()
        #LOG.debug(sout)
        return (json.loads(sout) if sout else None, serr)

    def main(self):
        from ec2sh import ec2sh
        from ec2stop import ec2stop
        from ec2list import ec2list
        cmds = {
            'sh' : ec2sh,
            'stop' : ec2stop,
            'ls' : ec2list
        }
        # Identify and instantiate command
        cmd_arg = sys.argv.pop(1)
        cmd_instance = cmds[cmd_arg]()
        # Invole command with arguments
        parser = argparse.ArgumentParser()
        parser.add_argument("-d", "--debug", help="Print debug info",action='store_true')
        sw = StopWatch().start()
        cmd_instance.run(parser)
        print "Command completed in %ssec" % sw.readSec()


def main():
    ec2().main()

if __name__ == '__main__':
   main()