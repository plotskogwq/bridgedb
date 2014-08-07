"""integration tests for BridgeDB ."""

from __future__ import print_function
from twisted.trial import unittest

import smtplib
from smtpd import SMTPServer
import asyncore
import threading
import Queue
import random
import time
import random

# ------------- SMTP Client Config
SMTP_DEBUG_LEVEL = 0  # set to 1 to see SMTP message exchange
BRIDGEDB_SMTP_SERVER_ADDRESS = "localhost"
BRIDGEDB_SMTP_SERVER_PORT = 6725
FROM_ADDRESS_TEMPLATE = "test%d@127.0.0.1" # %d is parameterised with a random integer to make the sender unique
MIN_FROM_ADDRESS = 1 # minimum value used to parameterise FROM_ADDRESS_TEMPLATE
MAX_FROM_ADDRESS = 10**8  # max value used to parameterise FROM_ADDRESS_TEMPLATE. Needs to be pretty big to reduce the chance of collisions
TO_ADDRESS = "bridges@torproject.org"
MESSAGE_TEMPLATE = """From: %s
To: %s
Subject: testing

get bridges"""

# ------------- SMTP Server Setup
# Setup an SMTP server which we use to check for responses
# from bridgedb. This needs to be done before sending the actual mail
LOCAL_SMTP_SERVER_ADDRESS = 'localhost'
LOCAL_SMTP_SERVER_PORT = 2525 # Must be the same as bridgedb's EMAIL_SMTP_PORT

class EmailServer(SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data):
        ''' Overridden from SMTP server, called whenever a message is received'''
        self.message_queue.put(data)

    def thread_proc(self):
        ''' This function runs in thread, and will continue looping 
        until the _stop Event object is set by the stop() function'''
        while self._stop.is_set() == False:
            asyncore.loop(timeout=0.0, count=1)
        # must close, or asyncore will hold on to the socket and subsequent tests will fail with 'Address not in use' 
        self.close()

    def start(self):
        self.message_queue = Queue.Queue()
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self.thread_proc)
        self._thread.setDaemon(True) # ensures that if any tests do fail, then threads will exit when the parent exits
        self._thread.start()

    @classmethod
    def startServer(cls):
        #print("Starting SMTP server on %s:%s" % (LOCAL_SMTP_SERVER_ADDRESS, LOCAL_SMTP_SERVER_PORT))
        server = EmailServer((LOCAL_SMTP_SERVER_ADDRESS, LOCAL_SMTP_SERVER_PORT), None)
        server.start()
        return server

    def stop(self):
        # signal thread_proc to stop
        self._stop.set()
        # wait for thread_proc to return (shouldn't take long)
        self._thread.join()        
        assert self._thread.is_alive() == False, "Thread is alive and kicking"

    def getAndCheckMessageContains(self, text, timeoutInSecs=2.0):
        #print("Checking for reponse")
        message = self.message_queue.get(block=True, timeout=timeoutInSecs)
        assert message.find(text) != -1, "Message did not contain text \"%s\". Full message is:\n %s" % (text, message)

    def checkNoMessageReceived(self, timeoutInSecs=2.0):
        try:
            self.message_queue.get(block=True, timeout=timeoutInSecs)
        except Queue.Empty:
            return True          
        assert False, "Found a message in the queue, but expected none"

def sendMail(fromAddress):
    #print("Connecting to %s:%d" % (BRIDGEDB_SMTP_SERVER_ADDRESS, BRIDGEDB_SMTP_SERVER_PORT))
    client = smtplib.SMTP(BRIDGEDB_SMTP_SERVER_ADDRESS, BRIDGEDB_SMTP_SERVER_PORT)
    client.set_debuglevel(SMTP_DEBUG_LEVEL)

    #print("Sending mail TO:%s, FROM:%s" % (TO_ADDRESS, fromAddress))
    result = client.sendmail(fromAddress, TO_ADDRESS, MESSAGE_TEMPLATE % (fromAddress, TO_ADDRESS))
    assert result == {}, "Failed to send mail"
    client.quit()

class SMTPTests(unittest.TestCase):
    def setUp(self):
        ''' Called at the start of each test, ensures that the SMTP server is running'''
        self.server = EmailServer.startServer()

    def tearDown(self):
        ''' Called after each test, ensures that the SMTP server is cleaned up'''
        self.server.stop()

    def test_getBridges(self):
        # send the mail to bridgedb, choosing a random email address
        sendMail(fromAddress=FROM_ADDRESS_TEMPLATE % random.randint(MIN_FROM_ADDRESS, MAX_FROM_ADDRESS))

        # then check that our local SMTP server received a response 
        # and that response contained some bridges
        self.server.getAndCheckMessageContains("Here are your bridges")

    def test_getBridges_rateLimitExceeded(self):
        # send the mail to bridgedb, choosing a random email address
        FROM_ADDRESS = FROM_ADDRESS_TEMPLATE % random.randint(MIN_FROM_ADDRESS, MAX_FROM_ADDRESS)
        sendMail(FROM_ADDRESS)

        # then check that our local SMTP server received a response 
        # and that response contained some bridges
        self.server.getAndCheckMessageContains("Here are your bridges")

	# send another request from the same email address
        sendMail(FROM_ADDRESS)

        # this time, the email response should not contain any bridges
        self.server.getAndCheckMessageContains("You have exceeded the rate limit. Please slow down!")

        # then we send another request from the same email address
        sendMail(FROM_ADDRESS)

        # now there should be no response at all (wait 1 second to make sure)
        self.server.checkNoMessageReceived(timeoutInSecs=1.0)

    def test_getBridges_stressTest(self):
        ''' Sends a large number of emails in a short period of time, and checks that 
            a response is received for each message '''
        NUM_MAILS = 100
        for i in range(NUM_MAILS):
            # Note: if by chance two emails with the same FROM_ADDRESS are generated, this test will fail
            # Setting 'MAX_FROM_ADDRESS' to be a high value reduces the probability of this occuring, but does not rule it out
            sendMail(fromAddress=FROM_ADDRESS_TEMPLATE % random.randint(MIN_FROM_ADDRESS, MAX_FROM_ADDRESS))

        for i in range(NUM_MAILS):
            self.server.getAndCheckMessageContains("Here are your bridges")

