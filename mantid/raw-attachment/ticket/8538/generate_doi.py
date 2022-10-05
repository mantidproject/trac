#!/usr/bin/env python
""" ICAT This utility will register a DOI for an investigation, dataset or datafile"""

from suds import WebFault
from suds.client import Client
from suds.transport.https import HttpAuthenticated
from getpass import getpass
import logging

logging.getLogger('suds.client').setLevel(logging.CRITICAL)

# ICAT_WSDL = 'https://icatisis.esc.rl.ac.uk:8181/ICATService/ICAT?wsdl'
ICAT_WSDL = 'https://icatdev.isis.cclrc.ac.uk/ICATService/ICAT?wsdl'
# DOI_WSDL = 'https://sig-03.esc.rl.ac.uk:8181/doi/DOIService?wsdl'
DOI_WSDL = 'https://topcatdev.isis.cclrc.ac.uk/doi/DOIWebService?wsdl'
FACILITY = 'ISIS'
ICAT_AUTH_TYPE = 'uows'


def logon_icat():
    """
    log on to ICAT
    """
    try:
        credentials = FACTORY.create("credentials")
        entry = FACTORY.create("credentials.entry")
        entry.key = 'username'
        entry.value = raw_input('ICAT Username:')
        credentials.entry.append(entry)
        entry = FACTORY.create("credentials.entry")
        entry.key = 'password'
        entry.value = getpass('ICAT password: ')
        credentials.entry.append(entry)
        session_id = ICAT_SERVICE.login(ICAT_AUTH_TYPE, credentials)
    except WebFault, e:
        print "ERROR - Cannot log on to " + FACILITY + " - " + str(e)
#         logout()
        exit(2)
    if VERBOSE >= 2:
        print "Logged on to " + FACILITY
    return session_id



print '\nThis utility will register a DOI for an investigation\n'
VERBOSE = 3

ICAT_CLIENT = Client(ICAT_WSDL)
FACTORY = ICAT_CLIENT.factory
ICAT_SERVICE = ICAT_CLIENT.service

DOI_CLIENT = Client(DOI_WSDL)
DOI_SERVICE = DOI_CLIENT.service

SESSION_ID = logon_icat()

while True:
    DATA_TYPE = raw_input('Object type: i, d or f:')
    if ((DATA_TYPE == "i") or (DATA_TYPE == "d")  or (DATA_TYPE == "f")):
        break
INVESTIGATION_ID = raw_input('Object id:')

try:
    if (DATA_TYPE == "i"):
        DOI_SERVICE.registerDatafileDOI(SESSION_ID, INVESTIGATION_ID)
        print ("\nNew DOI:" + DOI_SERVICE.registerInvestigationDOI(SESSION_ID, INVESTIGATION_ID))
    if (DATA_TYPE == "d"):
        DOI_SERVICE.registerDatafileDOI(SESSION_ID, INVESTIGATION_ID)
        print ("\nNew DOI:" + DOI_SERVICE.registerDatasetDOI(SESSION_ID, INVESTIGATION_ID))
    if (DATA_TYPE == "f"):
        DOI_SERVICE.registerDatafileDOI(SESSION_ID, INVESTIGATION_ID)
        print ("\nNew DOI:" + DOI_SERVICE.registerDatafileDOI(SESSION_ID, INVESTIGATION_ID))
except WebFault, e:
    print "inside try fail, oh darn!\n"    
    print str(e)
    ICAT_SERVICE.logout(SESSION_ID)
    exit(1)

ICAT_SERVICE.logout(SESSION_ID)
print '\nDONE\n'
exit(0)
