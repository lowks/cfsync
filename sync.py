#!/usr/bin/env python

import sys
import getopt
import os
from cfsync import Sync
import logging
import logging.config
import cloudfiles

def usage(name, args):
  print 'Usage: ' + name + ' [opts] container folder'
  print '-h, --help\tdisplay this message'
  print '-u, --user\tRackspace API username'
  print '-k, --key\tRackspace API key'

def main(argv):
  user = None
  key = None
  delete = False
  try:
    opts, args = getopt.getopt(argv, "hu:k:c:d", ["help", "user", "key", "container", "delete"])
  except getopt.GetoptError:
    Sync.usage()
    sys.exit(2)
  for opt, arg in opts:
    logging.debug("Processing opt: " + opt)
    if opt in ("-h", "--help"):
      Sync.usage(sys.argv[0], args)
      sys.exit()
    elif opt in ("-u", "--user"):
      user = arg
    elif opt in ("-k", "--key"):
      key = arg
    elif opt in ("-d", "--delete"):
      delete = True
  print "Authenticating..."
  conn = cloudfiles.get_connection(user, key)
  cfsync = Sync(conn)
  # cfsync.list_files(args[1])
  if delete:
    cfsync.clear(args[0])
  cfsync.upload(args[0], args[1])

if os.path.exists('logging.conf'):
  logging.config.fileConfig('logging.conf')
main(sys.argv[1:])