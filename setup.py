#!/usr/bin/env python

from distutils.core import setup

# patch distutils if it can't cope with the "classifiers" or
# "download_url" keywords
from sys import version
if version < '2.2.3':
    from distutils.dist import DistributionMetadata
    DistributionMetadata.classifiers = None
    DistributionMetadata.download_url = None

setup(name='Conficat',
      version='0.1',
      description='Generate configfiles from CSV tables and Cheetah templates',
      author='Lorenz Schori',
      author_email='lo@znerol.ch',
      url='http://www.znerol.ch/',
      license='FreeBSD License',
      requires=['Cheetah'],
      classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
      ],
      scripts=['scripts/conficat'],
      package_dir = {'Conficat':'lib'},
      packages = ['Conficat'],
)
