# -*- coding: utf-8 ; test-case-name: bridgedb.test.test_parse_versions ; -*-
#
# This file is part of BridgeDB, a Tor bridge distribution system.
#
# :authors: Isis Lovecruft 0xA3ADB67A2CDB8B35 <isis@torproject.org>
#           please also see AUTHORS file
# :copyright: (c) 2014 Isis Lovecruft
#             (c) 2007-2014, The Tor Project, Inc.
#             (c) 2007-2014, all entities within the AUTHORS file
# :license: see included LICENSE for information

"""Parsers for Tor version number strings.

.. py:module:: bridgedb.parse.versions
   :synopsis: Parsers for Tor version number strings.

bridgedb.parse.versions
=======================
::

 Version - Holds, parses, and does comparison operations for package version numbers.
..
"""

from twisted.python import util as txutil


class Version(txutil.Version):
    """Holds, parses, and does comparison operations for version numbers.

    :attr string major: The major version number.
    :attr string minor: The minor version number.
    :attr string micro: The micro version number.
    :attr string prerelease: Sometime, another number, though often suffixed
        with a `-`, `+`, or `#`.
    """

    def __init__(self, version, package=None):
        """Create a version object.

        Comparisons may be computed between instances of :class:`Version`s.

        :param string version: One of ``SERVER_VERSIONS``.
        :param string package: The package or program which we are creating a
            version number for, i.e. for "tor-0.2.5.1-alpha" the ``package``
            would be "tor".
        """
        if version.find('.') == -1:
            print("Version.__init__(): %r doesn't look like a version string!"
                  % version.__repr__())

        major, minor, micro, prerelease = ['' for x in xrange(4)]

        components = version.split('.')
        if len(components) > 0:
            try:
                prerelease = components.pop()
                micro      = components.pop()
                minor      = components.pop()
                major      = components.pop()
            except IndexError:
                pass
        super(Version, self).__init__(package, major, minor, micro, prerelease)
        
    def base(self):
        """Get the base version number (with prerelease).

        :rtype: string
        :returns: A version number, without the package/program name, and with
            the prefix (if available). For example: '0.2.5.1-alpha'.
        """
        prerelease = getPrefixedPrerelease()
        return '%d.%d.%d%s' % (self.major, self.minor, self.micro, prerelease)

    def getPrefixedPrerelease(self, separator='.'):
        """Get the prerelease string, prefixed by the separator ``prefix``.

        :param string separator: The separator to use between the rest of the
            version string and the :attr:`prerelease` string.
        :rtype: string
        :returns: The separator plus the ``prefix``, i.e. '.1-alpha'.
        """
        pre = ''
        if self.prerelease is not None:
            pre = prefix + self.prerelease
        return pre

    def __repr__(self):
        prerelease = getPrefixedPrerelease('')
        return '%s(package=%r, major=%d, minor=%d, micro=%d, prerelease=%s)' \
            % (self.__class__.__name__, str(self.package),
               self.major, self.minor, self.micro, self.prerelease)
