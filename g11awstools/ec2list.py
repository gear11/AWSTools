__author__ = 'Andy Jenkins'
import logging
import g11pyutils as utils
from ec2 import ec2
LOG = logging.getLogger("ec2list")


class ec2list(ec2):

    def get_non_none(self, dct, key, default):
        val = dct.get(key)
        return val if val else default

    def run(self, parser):
        """Lists ec2 instances"""
        parser.add_argument("-l", "--long", help="Long format.", action='store_true')


        args = self.parse_args(parser)

        # Ensure we have exactly 1 instance with the desired name
        keys = None
        for i in self.instances():
            props = [ i.get("Name") ]
            if args.long:
                if not keys:
                    keys = [ "InstanceId", "PublicDnsName", "State", "LaunchTime"]
                    fmt = "%-15s %-10s %-45s %-8s %s"
                    utils.print_bold(fmt % tuple(["ImageName"] + keys))
                props.append(self.get_non_none(i, keys[0], "None"))
                props.append(self.get_non_none(i, keys[1], "N/A"))
                props.append(self.get_non_none(i, keys[2], { "Name" : "N/A"})["Name"])
                props.append(self.get_non_none(i, keys[3], "N/A"))
            print fmt % tuple(props)


def main():
    ec2list().main()

if __name__ == '__main__':
    main()