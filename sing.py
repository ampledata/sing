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

def generate_events( filename, events ):
    write_path = os.path.join( '.', filename )
    if 'SPLUNK_HOME' in os.environ:
        write_path = os.path.join( os.environ['SPLUNK_HOME'], 'var', 'spool', 'splunk', filename )
    
    logger = logging.getLogger("sing")
    logger.setLevel(logging.DEBUG)
    file_logger         = logging.FileHandler( write_path, mode='w' )
    file_logger_format  = logging.Formatter( '%(asctime)s %(levelname)s %(message)s' )
    file_logger.setFormatter( file_logger_format )
    logger.addHandler( file_logger )    
    for e in range( 0, events ):
        logger.info( "sing" )


def get_total_event_count( indexer, username, password ):
    from splunk import entity, auth, mergeHostPath
    mergeHostPath( indexer, True )
    auth.getSessionKey( username=username, password=password )
    properties = entity.getEntity( entityPath='/data/indexes', entityName='main' ).properties
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
    parser.add_option("-f", "--file",       dest="filename",    default="sing.log", help="Write events to FILE.", metavar="FILE"     )
    parser.add_option("-e", "--events",     dest="events",      default=1,          help="Number of events to generate.", type="int" )
    parser.add_option("-i", "--indexer",    dest="indexer",                         help="Indexer to query for event count."         )
    parser.add_option("-u", "--username",   dest="username",    default='admin',    help="Username to auth against Indexer."         )
    parser.add_option("-p", "--password",   dest="password",    default='changeme', help="Username to auth against Indexer."         )
    parser.add_option("-s", "--show",       dest="show",                            help="Print event count.", action="store_true"   )
    (options, args) = parser.parse_args()

    if options.indexer:
        total_event_count = get_total_event_count( indexer=options.indexer, username=options.username, password=options.password )
        if options.show:
            print total_event_count
        return check_total_event_count( total_event_count=total_event_count, events=options.events )
    else:
        return generate_events( filename=options.filename, events=options.events )


if __name__ == "__main__":
	sys.exit(main())
