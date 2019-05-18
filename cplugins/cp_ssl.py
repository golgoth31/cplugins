r"""Get an SSL certificate from a website and extract useful data."""
# -*- coding: utf-8 -*-

# pybroker
# Copyright (c) 2016 David Sabatie <pybroker@notrenet.com>
#
# This file is part of Pybroker.
#
# Foobar is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Foobar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
# from .cp_options import CpOptions

import ssl
import time
import OpenSSL


class CpSSL():
    r"""Get an SSL certificate from a remote host and extract data from it.

    Attributes
    ----------
    host: str
        Host to be checked; FQDN or ip.
    port: str
        Port to connect to.

    """

    def __init__(self, host, port):
        """Init."""
        conn = ssl.create_connection((host, port))
        context = ssl.SSLContext()
        sock = context.wrap_socket(conn, server_hostname=host)
        cert = ssl.DER_cert_to_PEM_cert(sock.getpeercert(True))
        self._x509 = OpenSSL.crypto.load_certificate(
            OpenSSL.crypto.FILETYPE_PEM, cert
        )
        self._fmt_not_after = time.strptime(
            self._x509.get_notAfter().decode("utf-8"), "%Y%m%d%H%M%SZ"
        )

    def get_expiration_from_now(self):
        r"""Get time delta from now to expiration date.

        Returns
        -------
        int
            Number of remaining days.

        """
        not_after = time.mktime(self._fmt_not_after)
        now = time.time()
        remain = not_after - now
        return int(remain / 60 / 60 / 24)

    def get_expiration_date(self):
        r"""Get expiration date and format it as expected.

        Returns
        -------
        str
            Formated date.

        """
        return time.strftime("%b %d %H:%M:%S %Y", self._fmt_not_after)

    def get_subject(self):
        r"""Extract certificate subject.

        Returns
        -------
        str
            Subject from CN.

        """
        for name in self._x509.get_subject().get_components():
            if name[0] == b'CN':
                return name[1].decode("utf-8")
        return None

    def get_issuer(self):
        r"""Extract certificate issuer.

        Returns
        -------
        str
            Issuer from CN.

        """
        for name in self._x509.get_issuer().get_components():
            if name[0] == b'CN':
                return name[1].decode("utf-8")
        return None
