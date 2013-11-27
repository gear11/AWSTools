__author__ = 'jenkins'
import logging
from subprocess import Popen, PIPE, STDOUT
import json
import itertools
from g11pyutils import IndexedDictList

LOG = logging.getLogger("ec2")

class ec2:
    def start_instance(self, instance):
        """Starts the given EC2 instance, optionally blocking until it completes."""
        LOG.info("Starting EC2 instance %s" % instance["Name"])
        cmd = 'aws ec2 start-instances --instance-ids %s' % instance["InstanceId"]
        p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        s = p.stdout.read()
        LOG.debug(s)
        rsp = json.loads(s)

    def stop_instance(self, instance):
        """Starts the given EC2 instance, optionally blocking until it completes."""
        LOG.info("Stopping EC2 instance %s" % instance["Name"])
        cmd = 'aws ec2 stop-instances --instance-ids %s' % instance["InstanceId"]
        p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        s = p.stdout.read()
        LOG.debug(s)
        rsp = json.loads(s)

    def instances(self):
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
