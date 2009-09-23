#!/usr/bin/env python
"""
Test cases for checkrelpath conficat utility function
"""

import unittest
import os
import re
from Conficat.Util import checkrelpath
from Conficat.ValidationError import ValidationError
from tempfile import mkstemp, mkdtemp

class CheckrelpathsTestCase(unittest.TestCase):
  """
  Testcase for the checkrelpaths utility function 
  """

  def testCheckProperRelativePath(self):
    """
    A correctly formatted relative path must not throw an Exception
    """
    p="path/to/dir"
    self.assertEqual(p, checkrelpath(p))

  def testCheckRelativePathWithReferenceToEnclosingDir(self):
    """
    Checking a relative path pointing to an enclosing dir must throw an
    Exception
    """
    p="../path/to/dir"
    self.assertRaises(ValidationError, checkrelpath, p)

  def testCheckAbsolutePath(self):
    """
    Checking an absolute path must throw an Exception
    """
    p="/tmp"
    self.assertRaises(ValidationError, checkrelpath, p)

  def testCheckRelativePathWithNonObviousRefToEnclosingDir(self):
    """
    Checking a relative path pointing to an enclosing dir must throw an
    Exception
    """
    p="some/../../relative/./path"
    self.assertRaises(ValidationError, checkrelpath, p)

if __name__ == '__main__':
  unittest.main()
