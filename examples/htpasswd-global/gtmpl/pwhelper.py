#!/usr/bin/python
"""Replacement for htpasswd"""
# Original author: Eli Carter
# Modified version from Trac:
# http://trac.edgewall.org/browser/trunk/contrib/htpasswd.py

import sys
import random
from Cheetah.Template import Template

# We need a crypt module, but Windows doesn't have one by default.  Try to find
# one, and tell the user if we can't.
try:
    import crypt
except ImportError:
    try:
        import fcrypt as crypt
    except ImportError:
        sys.stderr.write("Cannot find a crypt module.  "
                         "Possibly http://carey.geek.nz/code/python-fcrypt/\n")
        sys.exit(1)

def __salt():
  """Returns a string of 2 randome letters"""
  letters = 'abcdefghijklmnopqrstuvwxyz' \
            'ABCDEFGHIJKLMNOPQRSTUVWXYZ' \
            '0123456789/.'
  return random.choice(letters) + random.choice(letters)

def htpasswd(password):
  return crypt.crypt(password, __salt())
