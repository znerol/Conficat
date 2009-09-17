#!/usr/bin/env python
"""
Test cases for conficat utility functions
"""
__author__ =  'Lorenz Schori'
__version__=  '0.1'

import unittest
import os
from Conficat.Util import parseCSVFiles
from tempfile import mkstemp

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

if __name__ == '__main__':
  unittest.main()
