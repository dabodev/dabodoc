#!/usr/bin/env python

import sys
import os
import shutil

def die(msg):
  sys.stderr.write('ERROR: ' + msg)
  sys.exit(1)
  
cwd = os.getcwd()
if not os.path.exists('book') \
   or not os.path.exists('Makefile'):
  die('Please run this from the Dabo book source directory\n')
  
if not os.getenv('JAVA_HOME'):
  die('JAVA_HOME is not set correctly.\n')

if os.path.exists('./usr'):
  die('Please remove ./usr.\n')

os.putenv('FOP_OPTS', '-Xms100m -Xmx200m')

os.system('DESTDIR=. make book-clean install-book-html ' + \
          'install-book-html-chunk install-book-pdf')

tarball = os.path.join(cwd, 'dabobook.tar.gz')

try:
  os.chdir('./usr/share/doc/dabo')
  os.rename('book', 'dabobook')
  os.system('tar cvfz ' + tarball + ' dabobook')
finally:
  os.chdir(cwd)
  shutil.rmtree('./usr')
  
if not os.path.exists(tarball):
  die('Hrm.  It appears the tarball was not created.\n')

print 'Your tarball sits in ./dabobook.tar.gz.  Enjoy!'
