import sys
import getopt
import os
import cloudfiles
import md5sum
import cfsync
from ssl import SSLError

class Sync(object):
  def __init__(self, user, key, logLevel = 'debug'):
    self.user = user
    self.key = key
    print "Authenticating..."
    self.conn = cloudfiles.get_connection(user, key)
    self.logLevel = logLevel

  def debug(self, msg):
    if self.logLevel == 'debug':
      print msg

  def compare(self, container, folder):
    container = self.conn.get_container(container)
    print container.list_objects()
    print self.list_files(folder)

  def upload(self, container, folder):
    cont  = self.conn.get_container(container)
    cont.enable_static_web('index.html')
    local_files = self.list_files(folder)
    total = len(local_files)
    for i,local_file in enumerate(local_files):
      print "#%d of %d"%(i+1,total)
      name = os.path.relpath(local_file, folder)
      # print name
      obj = cont.create_object(name)
      retry = 5
      try:
        etag = obj.etag
        checksum = md5sum.md5sum(local_file)
        self.debug("Etag: " + etag)
        self.debug("MD5SUM: " + checksum)
        if etag == checksum:
          print name + " matches!  Skipping..."
        else:
          obj.load_from_filename(local_file, True, callback)
      except SSLError, e:
        retry -= 1
        print "Retries left: %d"%(retry)
        if retry < 0:
          raise cloudfiles.errors.ResponseError(e)

  def clear(self, container):
    cont = self.conn.get_container(container)
    for obj in cont.list_objects():
      print 'Deleting: ' + obj
      cont.delete_object(obj)

  @staticmethod
  def list_files(folder):
    files = []
    for dirname, dirnames, filenames in os.walk(folder):
      for filename in filenames:
        fullfile = os.path.join(dirname, filename)
        fullfile = os.path.relpath(fullfile, folder)
        if not ".git" in fullfile:
          files.append(fullfile)
    return files

  @staticmethod
  def usage(args):
    if len(args) > 0:
      print args[0]
      if args[0] == 'config':
        c = cfsync.config.Config()
        c.usage()
    print 'Usage: ' + sys.argv[0] + ' [opts] container folder'
    print '-h, --help\tdisplay this message'
    print '-u, --user\tRackspace API username'
    print '-k, --key\tRackspace API key'

def callback(transferred, size):
  print "Transferred %d of %d"%(transferred,size)

def main(argv):
  user = None
  key = None
  try:
    opts, args = getopt.getopt(argv, "hu:k:c:", ["help", "user", "key", "container"])
  except getopt.GetoptError:
    Sync.usage()
    sys.exit(2)
  for opt, arg in opts:
    if opt in ("-h", "--help"):
      Sync.usage(args)
      sys.exit()
    elif opt in ("-u", "--user"):
      user = arg
    elif opt in ("-k", "--key"):
      key = arg
  cfsync = Sync(user, key)
  # cfsync.list_files(args[1])
  # cfsync.clear(args[0])
  cfsync.upload(args[0], args[1])


# conn = cloudfiles.get_connection(os.environ['RACKSPACE_USER'], os.environ['RACKSPACE_API_KEY'])
# container = conn.get_container('')

#main(sys.argv[1:])
