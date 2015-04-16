# BridgeDB by Nick Mathewson.
# Copyright (c) 2007-2012, The Tor Project, Inc.
# See LICENSE for licensing information 

from ipaddr import IPv6Address, IPv4Address
import logging

funcs = {}

def filterAssignBridgesToRing(hmac, numRings, assignedRing):
    #XXX: ruleset should have a key unique to this function
    # ruleset ensures that the same 
    logging.debug("Creating a filter for assigning bridges to hashrings...")
    ruleset = frozenset([hmac, numRings, assignedRing]) 

    try: 
        return funcs[ruleset]
    except KeyError:
        def _assignBridgesToRing(bridge):
            digest = hmac(bridge.getID())
            pos = long( digest[:8], 16 )
            which = pos % numRings + 1

            if which == assignedRing:
                return True
            return False
        _assignBridgesToRing.__name__ = ("filterAssignBridgesToRing(%s, %s, %s)"
                                         % (hmac, numRings, assignedRing))
        # XXX The `description` attribute must contain an `=`, or else
        # dumpAssignments() will not work correctly.
        setattr(_assignBridgesToRing, "description", "ring=%d" % assignedRing)
        funcs[ruleset] = _assignBridgesToRing
        return _assignBridgesToRing

def filterBridgesByRules(rules):
    ruleset = frozenset(rules)
    try: 
        return funcs[ruleset] 
    except KeyError:
        def g(x):
            r = [f(x) for f in rules]
            if False in r: return False
            return True
        setattr(g, "description", " ".join([getattr(f,'description','') for f in rules]))
        funcs[ruleset] = g
        return g  

def filterBridgesByIP4(bridge):
    try:
        if IPv4Address(bridge.address): return True
    except ValueError:
        pass

    for address, port, version in bridge.allVanillaAddresses:
        if version == 4:
            return True
    return False
setattr(filterBridgesByIP4, "description", "ip=4")

def filterBridgesByIP6(bridge):
    try:
        if IPv6Address(bridge.address): return True
    except ValueError:
        pass

    for address, port, version in bridge.allVanillaAddresses:
        if version == 6:
            return True
    return False
setattr(filterBridgesByIP6, "description", "ip=6")

def filterBridgesByTransport(methodname, addressClass=None):
    if not ((addressClass is IPv4Address) or (addressClass is IPv6Address)):
        addressClass = IPv4Address

    ruleset = frozenset([methodname, addressClass])
    try:
        return funcs[ruleset]
    except KeyError:

        def _filterByTransport(bridge):
            for transport in bridge.transports:
                if isinstance(transport.address, addressClass):
                    # ignore method name case
                    if transport.methodname.lower() == methodname.lower():
                        return True
            return False

        _filterByTransport.__name__ = ("filterBridgesByTransport(%s,%s)"
                                       % (methodname, addressClass))
        setattr(_filterByTransport, "description", "transport=%s" % methodname)
        funcs[ruleset] = _filterByTransport
        return _filterByTransport

def filterBridgesByNotBlockedIn(countryCode):
    """Return ``True`` if at least one of a bridge's (transport) bridgelines isn't
    known to be blocked in **countryCode**.

    :param str countryCode: A two-letter country code.
    :rtype: bool
    :returns: ``True`` if at least one address of the bridge isn't blocked.
        ``False`` otherwise.
    """
    countryCode = countryCode.lower()
    ruleset = frozenset([countryCode])
    try:
        return funcs[ruleset]
    except KeyError:
        def _filterByNotBlockedIn(bridge):
            if bridge.isBlockedIn(countryCode):
                return False
            return True
        _filterByNotBlockedIn.__name__ = "filterBridgesByNotBlockedIn(%s)" % countryCode
        setattr(_filterByNotBlockedIn, "description", "unblocked=%s" % countryCode)
        funcs[ruleset] = _filterByNotBlockedIn
        return _filterByNotBlockedIn
