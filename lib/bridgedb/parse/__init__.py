# -*- coding: utf-8 -*-
#
# This file is part of BridgeDB, a Tor bridge distribution system.
#
# :authors: Isis Lovecruft 0xA3ADB67A2CDB8B35 <isis@torproject.org>
#           please also see AUTHORS file
# :copyright: (c) 2013 Isis Lovecruft
#             (c) 2007-2013, The Tor Project, Inc.
#             (c) 2007-2013, all entities within the AUTHORS file
# :license: 3-clause BSD, see included LICENSE for information

"""Modules for parsing data.

** Package Overview: **

..
  parse
   ||_ parse.addr
   |   |_ isIPAddress - Check if an arbitrary string is an IP address.
   |   |_ isIPv4 - Check if an arbitrary string is an IPv4 address.
   |   |_ isIPv6 - Check if an arbitrary string is an IPv6 address.
   |   \_ isValidIP - Check that an IP address is valid.
   |
   |__ :mod:`bridgedbparse.headers`
   |__ :mod:`bridgedb.parse.options`
   \__ :mod:`bridgedb.parse.versions`
"""


def padBase64(b64string):
    """Re-add any stripped equals sign character padding to a b64 string.

    :param string b64string: A base64-encoded string which might have had its
        trailing equals sign padding removed.
    """
    try:
        b64string = b64string.strip()
    except AttributeError:
        logging.error("Cannot pad base64 string %r: not a string." % b64string)
    else:
        addchars  = 0
        remainder = len(b64string) % 4
        if 2 <= remainder <= 3:
            addchars = 4 - remainder
        else:
            raise ValueError("Invalid base64-encoded string: %r" % b64string)
        b64string += '=' * addchars
    finally:
        return b64string
