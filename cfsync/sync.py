import os
import cloudfiles
import md5sum
import cfsync
import logging
from ssl import SSLError

class Sync(object):
  def __init__(self, conn, logLevel = 'debug'):
    self.conn = conn
    self.logLevel = logLevel

  def compare(self, container, folder):
    container = self.conn.get_container(container)
    print container.list_objects()
    print Sync.list_files(folder)

  def upload(self, container, folder):
    cont  = self.conn.get_container(container)
    cont.enable_static_web('index.html')
    local_files = Sync.list_files(folder)
    total = len(local_files)
    for i,local_file in enumerate(local_files):
      print "#%d of %d"%(i+1,total)
      name = os.path.relpath(local_file, folder)
      # print name
      obj = cont.create_object(name)
      retry = 5
      try:
        etag = obj.etag
        logging.debug("Checking md5sum of " + name)
        checksum = md5sum.md5sum(os.path.join(folder, local_file))
        logging.debug("Etag: " + etag)
        logging.debug("MD5SUM: " + checksum)
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
    logging.info("Clearing container %s"%cont)
    for obj in cont.list_objects():
      logging.info('Deleting:%s'%obj)
      cont.delete_object(obj)

  @staticmethod
  def list_files(folder):
    files = []
    for dirname, dirnames, filenames in os.walk(folder):
      for filename in filenames:
        fullfile = os.path.join(dirname, filename)
        # fullfile = os.path.relpath(fullfile, folder)
        if not ".git" in fullfile:
          files.append(fullfile)
    return files

def callback(transferred, size):
  print "Transferred %d of %d"%(transferred,size)
