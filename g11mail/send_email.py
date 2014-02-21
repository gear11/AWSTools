import smtplib
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import argparse
import logging
import sys
import os

LOG = logging.getLogger("send_email")


class Mailer(object):
    """Encapsulates creating and sending an SMTP message.

    Usage:
        mailer = Mailer('abante.lunarpages.com:587', 'noreply@gear11.com', password)
        mailer.mail((args.to, args.cc, args.bcc), subject, [ [string_of_html, 'html' ] ])
        mailer.quit()
    """
    def __init__(self, server, user, password):
        self.user = user
        self.password = password
        self.server = smtplib.SMTP(server)

    def mail(self, addresses, subject, body_parts, filenames = None):
        """Compose and send an e-mail.

        Keyword arguments:
        addresses -- a tuple of (to, cc, bcc), each of which is a comma-delimited list of e-mail addresses
        subject -- the text subject of the e-mail
        body_parts -- a list of tuples of (body_test, mode) to append to the message
        filenames -- (optional) a list of filenames
        """
        (to_addr, cc_addr, bcc_addr) = addresses

        LOG.info("Creating message to %s", to_addr)
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['To'] = to_addr
        msg['From'] = self.user
        if cc_addr:
            msg['Cc'] = cc_addr

        LOG.info("Composing body elements")
        for (text, mode) in body_parts:
            LOG.info("Attaching text as %s", mode)
            part = MIMEText(text, mode)
            msg.attach(part)

        if filenames:
            LOG.info("Adding file attachements")
            for f in filenames:
                self.attach_file(msg, f)

        LOG.info("Sending e-mail")
        self.send(msg)
        LOG.info("E-mail sent")

    def quit(self):
        LOG.info("Closing server connection")
        self.server.quit()

    def attach_file(self, msg, afile):
        part = MIMEApplication(open(afile, "rb").read())
        part.add_header('Content-Disposition', 'attachment', filename=afile)
        msg.attach(part)

    def send(self, msg):
        self.server.ehlo()
        self.server.starttls()
        self.server.ehlo()
        self.server.login(self.user, self.password)

        to = msg['To']
        cc = msg['Cc']
        if cc:
            to = ",".join(to,cc)
        to = to.split(",")
        self.server.sendmail(msg['From'], to, msg.as_string())
        if msg['Bcc']:
            self.server.sendmail(msg['From'],msg['Bcc'].split(","),msg.as_string())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("to", help="TO emails, comma-delimited")
    parser.add_argument("file", help="The name of the file to e-mail")
    parser.add_argument("-p", "--password", help="E_mail server password")
    parser.add_argument("-s", "--subject", help="Subject, will default to the filename")
    parser.add_argument("-c", "--cc", help="CCs, comma-delimited", default="")
    parser.add_argument("-b", "--bcc", help="BCCs, comma-delimited", default="")
    parser.add_argument("-d", "--debug", help="Print debug info",action='store_true')
    parser.add_argument("-u", "--username", help="E-mail server username (and From)", default= 'noreply@gear11.com')
    parser.add_argument("-v", "--server", help="E-mail server and port", default='abante.lunarpages.com:587')
    args = parser.parse_args()

    level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(format='%(asctime)-15s %(levelname)s:%(name)s:%(message)s', level=level, stream=sys.stderr)

    LOG.info("Reading %s", args.file)
    fname = os.path.basename(args.file)
    ext = fname.rsplit('.', 1)[-1]
    mode = "html" if (ext == "html" or ext == "htm") else "text"
    with open(args.file) as f:
        body = f.read()
    LOG.info("Read %s (%s bytes)", fname, len(body))
    subject = args.subject if args.subject else fname
    LOG.info("Sending '%s' to %s", subject, args.to )

    mailer = Mailer(args.server, args.username, args.password)
    mailer.mail((args.to, args.cc, args.bcc), subject, [ (body, mode) ])
    mailer.quit()

if __name__ == '__main__':
    main()