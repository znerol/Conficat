#!/usr/bin/env python
"""
Data Source class for CSV data
"""

import csv
import os
import re
from stat import *
from ValidationError import ValidationError
from Util import findfiles

class CSVDataSource(object):
  def __init__(self):
    self.data={}

  def __iter__(self):
    for (key, value) in self.data.iteritems():
      yield (key, value)

  def __len__(self):
    return len(self.data)

  def __getitem__(self, key):
    return self.data[key]

  def __contains__(self, key):
    return self.data.has_key(key)

  def loadFromPath(self, path, strip='auto', prefix=[], *args, **kwds):
    """
    Load CSV data from the path which is either a file or a whole directory.
    """
    assert(isinstance(path, str))
    assert(isinstance(prefix, list))
    assert(strip == 'auto' or isinstance(strip, int))

    # Automatically strip everything off from up to the last path component if
    # specified otherwise
    if strip == 'auto':
      strip = len(os.path.normpath(path).lstrip("/.").split(os.path.sep))-1
      # Also remove the last component if this is a directory, or if a prefix was
      # specified.
      if os.path.isdir(path) or prefix != []:
        strip = strip+1

    # Loop thru csv files found in the dir (or just read in the file if the path
    # points to a single file)
    csvext=(lambda p: re.match(r'.+\.csv$',p.lower()) != None)
    for f in findfiles(path,csvext):
      (base, ignored_ext) = f.rsplit(".", 1)
      base = base.lstrip("/.")
      components = prefix + base.split(os.path.sep)[strip:]

      # descend to leaf
      leaf = self.data
      for c in components[0:-1]:
        if not leaf.has_key(c):
          leaf[c] = {}
        leaf = leaf[c]

      # copy rows
      leaf[components[-1]] = []
      for row in csv.DictReader(open(f,"rb"), *args, **kwds):
        newrow = {}
        for (key, val) in row.iteritems():
          parts = key.split(".")
          if len(parts) == 1:
            newrow[key] = val
            continue

          level = newrow
          for part in parts[0:-1]:
            if not level.has_key(part):
              level[part] = {}
            level = level[part]
          level[parts[-1]] = val

        leaf[components[-1]].append(newrow)

