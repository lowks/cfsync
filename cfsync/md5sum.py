import sys
import hashlib

def md5sum(file):
  md5 = hashlib.md5()
  with open(file,'rb') as f: 
      for chunk in iter(lambda: f.read(8192), b''): 
           md5.update(chunk)
  return md5.hexdigest()

# print md5sum(sys.argv[1])