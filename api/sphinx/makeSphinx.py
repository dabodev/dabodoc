# -*- coding: utf-8 -*-#

import os
import sys
import time
import shutil

# force it, otherwise the none ASCII stuff causes a problem for Sphinx
reload(sys)
sys.setdefaultencoding('utf-8')
del sys.setdefaultencoding

#import traceback
import subprocess

import glob

from config import *

def FractSec(s):

	min, s = divmod(s, 60)
	h, min = divmod(min, 60)
	return h, min, s

def MakeSphinx(builder, rebuildall):
	startupinfo = subprocess.STARTUPINFO()
	startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

	sourceFolder = docFolder
	targetFolder = os.path.join(os.path.join(baseFolder, 'build'), builder)
	confFolder = docFolder
	
	sErr = os.path.join(baseFolder, "sphinxstderr.txt")
	sphinxStdErr = open(sErr, 'wt')

	if rebuildall:
		# clear targetFolder
		shutil.rmtree(targetFolder, ignore_errors=True)

		# TO REBUILD ALL
		# sphinxErrFile is a dup of sphinxStdErr
		command = sphinxBuildCmd + ' -ac ' + confFolder +' -b '+ builder + graphVizDot + sourceFolder +' ' + targetFolder
	else:
		# TO REBUILD CHANGED
		command = sphinxBuildCmd + ' -c ' + confFolder +' -b '+ builder + graphVizDot + sourceFolder +' ' + targetFolder

	p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=None, stderr=sphinxStdErr, startupinfo=startupinfo).communicate()

	if builder == 'htmlhelp':
		hhpFile = os.path.join(os.path.join(targetFolder), 'helpdoc.hhp')
		command = hhpExe + hhpFile
		p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=None, stderr=sphinxStdErr, startupinfo=startupinfo).communicate()


start = time.time()

args = sys.argv[1:]

if not args:
	builder = normalHtml
	rebuildall = False
else:
	if len(args) != 2:
		print "you have to supply two args"
		print "e.g. 'html True' to use the html builder and force a full rebuild"
		sys.exit(2)
	else:
		if args[0] in ['html',]: # doesn't work yet, 'pdf']:
			builder = args[0]
		else:
			print "builder %s is not valid" % args[0]
			sys.exit(2)
		if args[1]:
			rebuildall = True
		else:
			rebuildall = False
	
MakeSphinx(builder, rebuildall)

current = time.time()
h, m, s = FractSec(int(current - start))

print "\nDabo Documentation Sphinx build '%s' is finished. Elapsed time %02d:%02d:%02d" % (builder, h, m, s)
