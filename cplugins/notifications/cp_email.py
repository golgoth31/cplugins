# -*- coding: utf-8 -*-

# Cplugins
# Copyright (c) 2016 David Sabatie <github@notrenet.com>
#
# This file is part of Cplugins.
#
# Cplugins is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Cplugins is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template


class CpEmail():
    def __init__(self, conf, args):
        self.conf = conf
        self.args = args
        me = self.conf['email']['centreon_user'] + \
            '@' + \
            self.conf['email']['centreon_domain']

        # Parse common informations between host and service notifications
        if self.args.parameters['service_state'] is '':
            self.args.parameters['ack_url'] = self.conf['centreon_url'] + \
                '/main.php?p=20202&o=hak&cmd=15&host_name=' + \
                self.args.parameters['host_name']
            self.service_html_str = service_text = ''
        else:
            self.args.parameters['ack_url'] = self.conf['centreon_url'] + \
                '/main.php?p=20201&o=svcak&cmd=15&host_name=' + \
                self.args.parameters['host_name'] + \
                '&service_description=' + \
                self.args.parameters['service_desc']
            self.service_html_str = self.service_html()
            service_text = 'Service: ' + \
                self.args.parameters['service_desc'] + '\n'

        # generate default output (preparing template usage)
        text_output_str = 'Type: ' + \
            self.args.parameters['notification_type'] + \
            '\nHost: ' + self.args.parameters['host_name'] + \
            '\n' + service_text + 'State: ' + \
            self.args.parameters['state'] + \
            '\nInfo: ' + \
            self.args.parameters['output'] + \
            '\nDate/Time: date_time'
        html_output_str = self.host_html()
        email_subject_str = "[CENTREON] " + \
            self.args.parameters['notification_type'] + \
            ' ' + \
            self.args.parameters['object_name'] + \
            ' [' + \
            self.args.parameters['state'] + \
            ']'

        # Create message container - the correct MIME type is
        # multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = email_subject_str
        msg['From'] = me
        msg['To'] = self.args.to

        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(text_output_str, 'plain')
        part2 = MIMEText(html_output_str, 'html')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(part2)

        # Send the message via local SMTP server.
        s = smtplib.SMTP('localhost')
        # sendmail function takes 3 arguments: sender's address, recipient's address
        # and message to send - here it is sent as one string.
        s.sendmail(me, self.args.to, msg.as_string())
        s.quit()

    def service_html(self):
        html = Template(
            """\
<tr bgcolor=#eeeeee>
    <td><b>Servicename:</b></td>
    <td><b><a href='$url/main.php?p=20201&o=svcd&host_name=$host_name&service_description=$serv_desc'>$serv_desc</a></b></td>
<tr>
<tr bgcolor=#fefefe>
    <td><b>Servicename:</b></td>
    <td><b><a href='$url/main.php?p=20201&o=svcd&host_name=$host_name&service_description=$serv_desc'>$serv_desc</a></b></td>
<tr>
        """
        )
        return html.substitute(
            url=self.conf['centreon_url'],
            ack_url=self.args.parameters['ack_url'],
            host_name=self.args.parameters['host_name'],
            serv_desc=self.args.parameters['service_desc']
        )

    def host_html(self):
        # define some colors
        if self.args.parameters['state'] == 'OK' or \
                self.args.parameters['state'] == 'UP':
            self.head_color = '#00b71a'
        elif self.args.parameters['state'] == 'WARNING':
            self.head_color = '#f48400'
        elif self.args.parameters['state'] == 'CRITICAL' or \
                self.args.parameters['state'] == 'DOWN':
            self.head_color = '#ff0000'
        else:
            self.head_color = '#000000'

        html = Template(
            """\
<html>
    <body>
        <table border=0 width='98%' cellpadding=0 cellspacing=0>
            <tr>
                <td valign='top'>
                    <table border=0 cellpadding=0 cellspacing=0 width='98%'>
                        <tr bgcolor=$head_color>
                            <td width='140'>
                                <font color=#ffffff>
                                <b>Notification: </b>
                                </font>
                            </td>
                            <td>
                                <font color=#ffffff>
                                <b> $notification_type $object_name [$state]</b>
                                </font>
                            </td>
                        </tr>
                        <tr bgcolor=#fefefe>
                            <td><b>Hostname:</b></td>
                            <td><a href='$url/main.php?p=20202&o=hd&host_name=$host_name'>$host_alias</a></td>
                        <tr>
                        $service_html
                        <tr bgcolor=#eeeeee>
                            <td><b>Date/Time:</b></td>
                            <td>$long_date_time UTC</td>
                        </tr>
                        <tr bgcolor=#fefefe>
                            <td><b>Additional Info:</b></td>
                            <td><font color=$head_color>$output</font></td>
                        </tr>
                        <tr bgcolor=#eeeeee>
                            <td><b>Action:</b></td>
                            <td><a href='$ack_url'><b>Acknowledge</b></a></td>
                        <tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
</html>
        """
        )
        out = html.substitute(
            ack_url=self.args.parameters['ack_url'],
            output=self.args.parameters['output'],
            long_date_time=self.args.parameters['long_date_time'],
            service_html=self.service_html_str,
            url=self.conf['centreon_url'],
            head_color=self.head_color,
            notification_type=self.args.parameters['notification_type'],
            object_name=self.args.parameters['object_name'],
            state=self.args.parameters['state'],
            host_name=self.args.parameters['host_name'],
            host_alias=self.args.parameters['host_name']
        )
        return out
