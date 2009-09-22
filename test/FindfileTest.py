#!/usr/bin/env python
"""
Test cases for findfile conficat utility function
"""

import unittest
import os
import re
from Conficat.Util import findfiles
from tempfile import mkstemp, mkdtemp

class FindfilesTestCase(unittest.TestCase):
  """
  Testcase for the findfiles utility function 
  """
  def setUp(self):
    """create temporary directory and files"""
    self.empty_tmpdir = mkdtemp()
    self.pop_outer_tmpdir = mkdtemp()

    (ignored_fd, self.txt_outer) = mkstemp(suffix=".txt", dir=self.pop_outer_tmpdir)
    self.pop_inner_tmpdir = mkdtemp(dir=self.pop_outer_tmpdir)

    (ignored_fd, self.txt_inner) = mkstemp(suffix=".txt", dir=self.pop_inner_tmpdir)

  def tearDown(self):
    """cleanup temporary files and directories"""
    os.unlink(self.txt_inner)
    os.unlink(self.txt_outer)
    os.removedirs(self.pop_inner_tmpdir)
#    os.removedirs(self.pop_outer_tmpdir)
    os.removedirs(self.empty_tmpdir)
  
  def testCollectfilesExistingSinglefile(self):
    """findfiles must return exactly one entry for a single file"""
    txt_inner_iter = findfiles(self.txt_inner)
    self.assertEqual(self.txt_inner, txt_inner_iter.next())
    self.assertRaises(StopIteration, txt_inner_iter.next)

  def testCollectfilesExistingSinglefileMatchCriteria(self):
    """
    findfiles must return exactly one entry for a single file if the testfunc
    reports true for that file.
    """
    txt_inner_iter = findfiles(self.txt_inner, testfunc = lambda p:True)
    self.assertEqual(self.txt_inner, txt_inner_iter.next())
    self.assertRaises(StopIteration, txt_inner_iter.next)

  def testCollectfilesExistingSinglefileWrongNoMatchCriteria(self):
    """
    findfiles must not report any entry if the testfunc reports false for that
    file
    """
    txt_inner_iter = findfiles(self.txt_inner, testfunc = lambda p:False)
    self.assertRaises(StopIteration, txt_inner_iter.next)

  def testCollectfilesEmptyDirectory(self):
    """findfiles must not return any entry for empty directory"""
    for x in findfiles(self.empty_tmpdir):
      self.fail()

  def testCollectfilesPopulatedDirectory(self):
    """findfiles must report one entry for the populated test directory"""
    txt_inner_iter = findfiles(self.pop_inner_tmpdir)
    self.assertEqual(self.txt_inner, txt_inner_iter.next())
    self.assertRaises(StopIteration, txt_inner_iter.next)

  def testCollectfilesPopulatedDirectoryCorrectExtension(self):
    """
    findfiles must report one entry for the populated test directory if
    the extension parameter contains the txt extension.
    """
    txt_inner_iter = findfiles(self.pop_inner_tmpdir, testfunc = lambda p:True)
    self.assertEqual(self.txt_inner, txt_inner_iter.next())
    self.assertRaises(StopIteration, txt_inner_iter.next)

  def testCollectfilesPopulatedDirectoryWrongExtension(self):
    """
    findfiles must not report any entry for the populated test directory if
    the extension parameter does not contain the correct extension of the
    testfile
    """
    txt_inner_iter = findfiles(self.pop_inner_tmpdir, testfunc = lambda p:False)
    self.assertRaises(StopIteration, txt_inner_iter.next)

  def testCollectfilesNonExistantPath(self):
    """
    findfiles must report an OSError for non-existant paths
    """
    txt_inner_iter = findfiles(os.path.join(self.empty_tmpdir,"nothing"))
    self.assertRaises(OSError, txt_inner_iter.next)

if __name__ == '__main__':
  unittest.main()
