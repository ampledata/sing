#!/usr/bin/env python2.5
# encoding: utf-8
"""sing.py - Generate events or query event count on an Indexer.

WHY?
====
    Splunk + Ping = Sing.
    Good for testing forwarding Splunk setups.

USAGE
=====
    $ sing.py -e 1
    Generate 1 event in $SPLUNK_HOME/var/spool/splunk/sing.log if SPLUNK_HOME is set, otherwise ./sing.log.
    $ sing.py -e 1 -i https://splunk.example.com:8089
    Query splunk.example.com and exit 0 if event count is >= 1, otherwise exit 1.

NOTES
=====
    The Splunk SDK is not required to generate events, but is required to query event count.
    The Splunk SDK is bundled with every Splunk installation.
    For more information on Splunk, please see http://www.splunk.com/
    
META
====
    Created by Greg Albrecht gba@gregalbrecht.com
    Copyright 2010 Splunk, Inc. All rights reserved.
"""
__author__  = "Greg Albrecht gba@gregalbrecht.com"
__version__ = "1.0"
__license__ = "Copyright 2010 Splunk, Inc."

import os
import sys
import logging
from optparse import OptionParser

def generate_events( events=0, filename=None ):
    if filename:
        write_path = os.path.join( '.', filename )
    elif 'SPLUNK_HOME' in os.environ:
        write_path = os.path.join( os.environ['SPLUNK_HOME'], 'var', 'spool', 'splunk', 'sing.log' )
    else:
        write_path = os.path.join( '.', 'sing.log' )
    
    logger = logging.getLogger("sing")
    logger.setLevel(logging.DEBUG)
    file_logger         = logging.FileHandler( write_path, mode='w' )
    file_logger_format  = logging.Formatter( '%(asctime)s %(levelname)s %(message)s' )
    file_logger.setFormatter( file_logger_format )
    logger.addHandler( file_logger )    
    for e in range( 0, events ):
        logger.info( "sing" )


def get_total_event_count( server, index, username, password ):
    from splunk import entity, auth, mergeHostPath
    mergeHostPath( server, True )
    auth.getSessionKey( username=username, password=password )
    properties = entity.getEntity( entityPath='/data/indexes', entityName=index ).properties
    if 'totalEventCount' in properties:
        return int( properties['totalEventCount'] )
    else:
        return 0


def check_total_event_count( total_event_count, events ):
    if total_event_count >= events:
        return 0
    return 1


def main():
    parser = OptionParser()
    parser.add_option( "-e", "--events", dest="events", type="int", default=0, \
                       help="Number of events to generate." )
    parser.add_option( "-f", "--filename", dest="filename", metavar="FILENAME", \
                       help="Write events to FILENAME." )
    parser.add_option( "-i", "--index", dest="index", default="main", \
                       help="Index to query for event count." )
    parser.add_option( "-p", "--password", dest="password", default='changeme', \
                       help="Username to auth against Indexer." )
    parser.add_option( "-r", "--report", dest="report", action="store_true", \
                       help="Return the event count on the server." )
    parser.add_option( "-s", "--server", dest="server", \
                       help="Server to query." )
    parser.add_option( "-u", "--username", dest="username", default='admin', \
                       help="Username to auth against Indexer." )
    (options, args) = parser.parse_args()
    
    if options.server:
        total_event_count = get_total_event_count( server=options.server, index=options.index, \
                                                    username=options.username, password=options.password )
        if options.report:
            print total_event_count
        return check_total_event_count( total_event_count=total_event_count, events=options.events )
    else:
        return generate_events( events=options.events, filename=options.filename )


if __name__ == "__main__":
	sys.exit(main())
