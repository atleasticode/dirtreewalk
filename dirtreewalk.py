#!/usr/bin/python
# ‐*‐ coding: utf‐8 ‐*‐

"""
dirtreewalk.

Programme to list all files and subdirectories of a given directory path. 
The MD5 sum is calculated for every file.

Usage:
  dirtreewalk.py <pathname>...
  dirtreewalk.py -h | --help
  dirtreewalk.py --version

Options:
  -h --help     Show this information.
  --version     Show version.

"""

from docopt import docopt
import os, sys, hashlib

__author__ = "Lisa Trage"

'''
Function to recursively list all subdirectories and files of a given directory.
'''
def treewalk(path):
  try:
    all_files = os.listdir(path)
  except (PermissionError):
      print('You do not have permissions to read from this directory: {}.'.format(path))
      return
  except (FileNotFoundError, TypeError):
      print ('You did not enter a valid path.')
      return

  for item in all_files:
    full_path = os.path.join(path,item)
    rel_path = create_rel_path(path, item)
    
    if os.path.isdir(full_path):
      print("<directory>".ljust(15, ' '), item.ljust(40, ' '), rel_path.ljust(40, ' '))
      treewalk(full_path)

    elif os.path.isfile(full_path):
      print("<file>".ljust(15, ' '), item.ljust(40, ' '), rel_path.ljust(40, ' '), calculate_md5_sum(item))

    elif os.path.islink(full_path):
      print("<link>".ljust(15, ' '), item.ljust(40, ' '), rel_path.ljust(40, ' '))

    else:
      pass



'''
Function to calculate the MD5 sum of a file.
'''
def calculate_md5_sum(item):
  return hashlib.md5(item.encode('utf-8')).hexdigest()



'''
Function to return the path relative to the given directory.
All leading symbols (e.g. ../../example) are removed and the file that
was passed to the function is appended in the end.
'''
def create_rel_path(path, item):
  rel_path = os.path.relpath(path, start=os.path.curdir)
  rel_path = rel_path.split('/')
  rel_path.append(item)
  try: 
    rel_path = [x for x in rel_path if x != '..']
  except ValueError:
    pass
  rel_path.remove(rel_path[0])
  rel_path= '/'.join(rel_path)
  return rel_path



if __name__ == '__main__':
    arguments = docopt(__doc__, version='dirtreewalk 1.0')
    treewalk((arguments['<pathname>'][0]))
    
    