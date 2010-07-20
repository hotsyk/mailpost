"""
This code was adapted from iGmail http://butterfat.net/igmail/ Copyright (C)
2006 Brian Muller <bmuller@butterfat.net> which was in turn adapted from
"Twisted Network Programming Essentials" by Abe Fettig (ISBN 0-596-10032-9)
as published by O'Reilly.
All changes and additional code are Copyright (C) 2010 Devon Jones
<soulcatcher@evilsoft.org> and available under the terms of the GPL Version 2.
"""
import sys
from optparse import OptionParser

from twisted.cred import portal, checkers, credentials
from twisted.mail import imap4
from twisted.internet import protocol, reactor
from twisted.python import log, logfile


class Account:
    __implements__ = (imap4.IAccount,)

    def addMailbox(self, name, mbox=None):
        pass

    def create(self, pathspec):
        pass

    def select(self, name, rw=True):
        pass

    def delete(self, name):
        pass

    def rename(self, oldname, newname):
        pass

    def isSubscribed(self, name):
        pass

    def subscribe(self, name):
        pass

    def unsubscribe(self, name):
        pass

    def listMailboxes(self, ref, wildcard):
        pass

class Mailbox:
    __implements__ = (imap4.IMailbox,)

    def getUIDValidity(self):
        pass

    def getUIDNext(self):
        pass

    def getUID(self, message):
        pass

    def getMessageCount(self):
        pass

    def getRecentCount(self):
        pass

    def getUnseenCount(self):
        pass

    def isWriteable(self):
        pass

    def destroy(self):
        pass

    def requestStatus(self, names):
        pass

    def addListener(self, listener):
        pass

    def removeListener(self, listener):
        pass

    def addMessage(self, message, flags=(), date=None):
        pass

    def expunge(self):
        pass

    def fetch(self, messages, uid):
        pass

    def store(self, messages, flags, mode, uid):
        pass

class IMAPServerProtocol(imap4.IMAP4Server):
    "Subclass of imap4.IMAP4Server that adds debugging."
    debug = False

    def lineReceived(self, line):
        if self.debug:
            print "CLIENT:", line
        imap4.IMAP4Server.lineReceived(self, line)

    def sendLine(self, line):
        imap4.IMAP4Server.sendLine(self, line)
        if self.debug:
            print "SERVER:", line

class IMAPFactory(protocol.Factory):
    protocol = IMAPServerProtocol
    portal = None # placeholder

    def buildProtocol(self, address):
        p = self.protocol()
        p.portal = self.portal
        p.factory = self
        return p

class NoopCredentialsChecker:
    __implements__ = (checkers.ICredentialsChecker,)
    credentialInterfaces = (credentials.IUsernamePassword, credentials.IUsernamePassword)

    def requestAvatarId(self, credentials):
        return checkers.ANONYMOUS

def logout():
    pass
    # Cleanup logic goes here

class MailUserRealm:
    __implements__ = (portal.IRealm,)

    def requestAvatar(self, avatarID, mind, *interfaces):
        if imap4.IAccount not in interfaces:
            raise NotImplementedError
        return imap4.IAccount, Account(), logout


def main():
    usage = "usage: %prog [options]\n\n"
    parser = option_parser(usage)
    (options, args) = parser.parse_args()

    port = 143

    log.startLogging(sys.stdout)
    p = portal.Portal(MailUserRealm())
    p.registerChecker(NoopCredentialsChecker())
    factory = IMAPFactory()
    factory.portal = p

    reactor.listenTCP(port, factory)
    reactor.run()

def option_parser(usage):
    parser = OptionParser(usage=usage)
    return parser

if __name__ == "__main__":
    main()