# BridgeDB i18n strings & helper routines. The string should go into pootle

import os
import gettext

def getLang(lang, localedir=os.path.expanduser("~") + "/share/locale"):
    """Return the Translation instance for a given language. If no Translation
       instance is found, return the one for 'en'
    """
    return gettext.translation("bridgedb", localedir=localedir, 
                               languages=[lang], fallback="en")

def _(text):
    """This is necessary because strings are translated when they're imported.
       Otherwise this would make it impossible to switch languages more than 
       once
    """
    return text

# All text that needs translation goes here
BRIDGEDB_TEXT = [
 # BRIDGEDB_TEXT[0]
 _("""Here are your bridge relays: """),
 # BRIDGEDB_TEXT[1]
 _("""Bridge relays (or "bridges" for short) are Tor relays that aren't listed
in the main directory. Since there is no complete public list of them,
even if your ISP is filtering connections to all the known Tor relays,
they probably won't be able to block all the bridges."""),
 # BRIDGEDB_TEXT[2]
 _("""To use the above lines, go to Vidalia's Network settings page, and click
"My ISP blocks connections to the Tor network". Then add each bridge
address one at a time."""),
 # BRIDGEDB_TEXT[3]
 _("""Configuring more than one bridge address will make your Tor connection
more stable, in case some of the bridges become unreachable."""),
 # BRIDGEDB_TEXT[4]
 _("""Another way to find public bridge addresses is to send mail to
bridges@torproject.org with the line "get bridges" by itself in the body
of the mail. However, so we can make it harder for an attacker to learn
lots of bridge addresses, you must send this request from an email address at
one of the following domains:"""),
 # BRIDGEDB_TEXT[5]
 _("""[This is an automated message; please do not reply.]"""),
 # BRIDGEDB_TEXT[6]
 _("""Another way to find public bridge addresses is to visit
https://bridges.torproject.org/. The answers you get from that page
will change every few days, so check back periodically if you need more
bridge addresses."""),
 # BRIDGEDB_TEXT[7]
 _("""(no bridges currently available)"""),
 # BRIDGEDB_TEXT[8]
 _("""(e-mail requests not currently supported)"""),
 # BRIDGEDB_TEXT[9]
 _("""To receive your bridge relays, please prove you are human"""),
 # BRIDGEDB_TEXT[10]
 _("""You have exceeded the rate limit. Please slow down, the minimum time
between emails is: """),
 # BRIDGEDB_TEXT[11]
 _("""hours"""),
 # BRIDGEDB_TEXT[12]
 _("""All further emails will be ignored."""),
 # BRIDGEDB_TEXT[13]
 _("""Type the two words"""),
 # BRIDGEDB_TEXT[14]
 _("""I am human"""),
 # BRIDGEDB_TEXT[15]
 _("""Upgrade your browser to Firefox"""),
 # BRIDGEDB_TEXT[16]
 _("""(Might be blocked)"""),
 # BRIDGEDB_TEXT[17]
 _("""The following commands are also supported:"""),
 # BRIDGEDB_TEXT[18]
 _("""ipv6 : request ipv6 bridges."""),
 # BRIDGEDB_TEXT[19]
 _("""transport NAME : request transport NAME. Example: 'transport obfs2'"""),
 # BRIDGEDB_TEXT[20]
 _("""Looking for IPv6 bridges?"""),
 # BRIDGEDB_TEXT[21]
 _("""Looking for obfsproxy bridges?"""),
 # BRIDGEDB_TEXT[22]
 _("""Specify transport by name:"""),
 # BRIDGEDB_TEXT[23]
 _("""Submit""")
]
