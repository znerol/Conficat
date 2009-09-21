#!/usr/bin/env python
"""
Configuration utility functions
"""
__author__ =  'Lorenz Schori'
__version__=  '0.1'

from ConfigError import ConfigError

def checkfilemap(map, key, path):
  """
  Check a file key against a map (e.g. csvmap, tmplmap, etc). Raises a
  ConfigError if something is wrong with the key (duplicate, invalid)
  """
  if key==None or not re.match(r'^[a-zA-Z0-9_]+$', key):
    raise ConfigError("Invalid key %s for path %s", (key, path))
  if key in map:
    raise ConfigError("Duplicated key %s for path %s", (key, path))

def collectuniquefiles(keys, path, extensions):
  """
  recursively collect files from path with given extensions, split them
  up in filepath, basename and extension, check for duplication of base,
  also check syntax of base and yield results.
  """
  try:
    for (f, base, ext) in mapfiles(collectfiles(path, extensions)):
      checkfilemap(keys, base, path)
      yield (f, base, ext)
  except OSError, (errno, message):
    raise ConfigError("%s: %s (%d)", f, message, errno)

