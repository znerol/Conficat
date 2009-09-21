#!/usr/bin/env python
"""
Test cases for conficat utility functions
"""
__author__ =  'Lorenz Schori'
__version__=  '0.1'

import unittest
import os
from Conficat.Util import parseCSVFiles, collectfiles
from tempfile import mkstemp, mkdtemp

class ParseCSVFilesTestCase(unittest.TestCase):
  """ Test cases for parseCSVFile utility function"""

  csvrec="ID,Name\n1,Marvin\n"
  csvdict=dict(ID="1",Name="Marvin")
  fkey1="listtest"
  fkey2="dicttest"

  def setUp(self):
    (self.tmpfd, self.csvfile) = mkstemp(prefix="%s," % ParseCSVFilesTestCase.fkey1)
    f=open(self.csvfile,"w")
    f.write(ParseCSVFilesTestCase.csvrec)
    f.close()

    self.flist=[self.csvfile]
    self.fdict={ParseCSVFilesTestCase.fkey2:self.csvfile}

  def tearDown(self):
    os.unlink(self.csvfile)

  def testInvalidParametersFiles(self):
    for p in (list(),dict()):
      self.assertRaises(AssertionError,parseCSVFiles,p)

    for p in (23,"somestring",None,True,False):
      self.assertRaises(AssertionError,parseCSVFiles,p)

  def testValidCSVFileList(self):
    """test the structure and content of the resulting dictionary"""

    # first variant: use a list as a parameter
    result1 = parseCSVFiles(self.flist)
    self.assertTrue(isinstance(result1,dict))
    self.assertTrue(result1.has_key(ParseCSVFilesTestCase.fkey1))

    fkey1list=result1[ParseCSVFilesTestCase.fkey1]
    self.assertTrue(isinstance(fkey1list,list))
    self.assertTrue(len(fkey1list)==1)

    fkey1contents=fkey1list[0]
    self.assertTrue(isinstance(fkey1contents,dict))
    self.assertTrue(len(fkey1contents)==len(ParseCSVFilesTestCase.csvdict))

    for (key,value) in fkey1contents.iteritems():
      self.assertTrue(ParseCSVFilesTestCase.csvdict.has_key(key))
      self.assertEqual(ParseCSVFilesTestCase.csvdict[key],value)

  def testValidCSVFileDict(self):
    """test the structure and content of the resulting dictionary"""

    # first variant: use a list as a parameter
    result1 = parseCSVFiles(self.fdict)
    self.assertTrue(isinstance(result1,dict))
    self.assertTrue(result1.has_key(ParseCSVFilesTestCase.fkey2))

    fkey2list=result1[ParseCSVFilesTestCase.fkey2]
    self.assertTrue(isinstance(fkey2list,list))
    self.assertTrue(len(fkey2list)==1)

    fkey2contents=fkey2list[0]
    self.assertTrue(isinstance(fkey2contents,dict))
    self.assertTrue(len(fkey2contents)==len(ParseCSVFilesTestCase.csvdict))

    for (key,value) in fkey2contents.iteritems():
      self.assertTrue(ParseCSVFilesTestCase.csvdict.has_key(key))
      self.assertEqual(ParseCSVFilesTestCase.csvdict[key],value)

class CollectfilesTestCase(unittest.TestCase):
  """
  Testcase for the collectfiles utility function 
  """
  def setUp(self):
    """create temporary directory and files"""
    self.empty_tmpdir = mkdtemp()
    self.populated_tmpdir = mkdtemp()
    (ignored_fd, self.txt_tmpfile) = mkstemp(suffix=".txt",
                                             dir=self.populated_tmpdir)

  def tearDown(self):
    """cleanup temporary files and directories"""
    os.unlink(self.txt_tmpfile)
    os.removedirs(self.populated_tmpdir)
    os.removedirs(self.empty_tmpdir)
  
  def testCollectfilesExistingSinglefile(self):
    """collectfiles must return exactly one entry for a single file"""
    txt_tmpfile_iter = collectfiles(self.txt_tmpfile)
    self.assertEqual(self.txt_tmpfile, txt_tmpfile_iter.next())
    self.assertRaises(StopIteration, txt_tmpfile_iter.next)

  def testCollectfilesExistingSinglefileCorrectExtension(self):
    """
    collectfiles must return exactly one entry for a single file if the
    extension parameter contains the txt extension.
    """
    txt_tmpfile_iter = collectfiles(self.txt_tmpfile,extensions=["txt","bla"])
    self.assertEqual(self.txt_tmpfile, txt_tmpfile_iter.next())
    self.assertRaises(StopIteration, txt_tmpfile_iter.next)

  def testCollectfilesExistingSinglefileWrongExtension(self):
    """
    collectfiles must not report any entry if the extension parameter does
    not contain the correct extension of the testfile
    """
    txt_tmpfile_iter = collectfiles(self.txt_tmpfile,extensions=["zz","bla"])
    self.assertRaises(StopIteration, txt_tmpfile_iter.next)

  def testCollectfilesEmptyDirectory(self):
    """collectfiles must not return any entry for empty directory"""
    for x in collectfiles(self.empty_tmpdir):
      self.fail()

  def testCollectfilesPopulatedDirectory(self):
    """collectfiles must report one entry for the populated test directory"""
    txt_tmpfile_iter = collectfiles(self.populated_tmpdir)
    self.assertEqual(self.txt_tmpfile, txt_tmpfile_iter.next())
    self.assertRaises(StopIteration, txt_tmpfile_iter.next)

  def testCollectfilesPopulatedDirectoryCorrectExtension(self):
    """
    collectfiles must report one entry for the populated test directory if
    the extension parameter contains the txt extension.
    """
    txt_tmpfile_iter = collectfiles(self.populated_tmpdir,
        extensions=["txt","blabla","test"])
    self.assertEqual(self.txt_tmpfile, txt_tmpfile_iter.next())
    self.assertRaises(StopIteration, txt_tmpfile_iter.next)

  def testCollectfilesPopulatedDirectoryWrongExtension(self):
    """
    collectfiles must not report any entry for the populated test directory if
    the extension parameter does not contain the correct extension of the
    testfile
    """
    txt_tmpfile_iter = collectfiles(self.populated_tmpdir,
        extensions=["xy","blabla","test"])
    self.assertRaises(StopIteration, txt_tmpfile_iter.next)

  def testCollectfilesNonExistantPath(self):
    """
    collectfiles must report an OSError for non-existant paths
    """
    txt_tmpfile_iter = collectfiles(os.path.join(self.empty_tmpdir,"nothing"))
    self.assertRaises(OSError, txt_tmpfile_iter.next)

if __name__ == '__main__':
  unittest.main()
