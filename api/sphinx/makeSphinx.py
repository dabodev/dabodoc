# -*- coding: utf-8 -*-#

import os
import sys
import time
import shutil
import stat
import platform

# force it, otherwise the none ASCII stuff causes a problem for Sphinx
reload(sys)
sys.setdefaultencoding('utf-8')
del sys.setdefaultencoding

import subprocess

import config as sc

def FractSec(s):

	min, s = divmod(s, 60)
	h, min = divmod(min, 60)
	return h, min, s

def MakeSphinx(builder, rebuildall):
	if platform.system() == "Windows":
		startupinfo = subprocess.STARTUPINFO()
		startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

	sourceFolder = sc.docFolder
	targetFolder = os.path.join(os.path.join(sc.baseFolder, 'build'), builder)
	confFolder = sc.docFolder

	if rebuildall:
		# clear targetFolder
		shutil.rmtree(targetFolder, ignore_errors=True)

		# TO REBUILD ALL
		# sphinxErrFile is a dup of sphinxStdErr
		command = sc.sphinxBuildCmd + ' -ac ' + confFolder +' -b '+ builder + \
				sc.graphVizDot + sourceFolder +' ' + targetFolder
		commandArgs = [sc.sphinxBuildCmd, ' -ac ', confFolder, ' -b ', builder,
				sc.graphVizDot, sourceFolder, ' ', targetFolder]
	else:
		# TO REBUILD CHANGED
		command = sc.sphinxBuildCmd + ' -c ' + confFolder +' -b '+ builder + \
				sc.graphVizDot + sourceFolder +' ' + targetFolder
		commandArgs = [sc.sphinxBuildCmd, ' -c ' + confFolder, ' -b ', builder, \
				sc.graphVizDot, sourceFolder, ' ', targetFolder]

	if platform.system() == "Windows":
		p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=None,
			stderr=sc.sphinxStdErrFile, startupinfo=startupinfo).communicate()
	else:
		p = subprocess.Popen(commandArgs, stdin=subprocess.PIPE, stdout=None,
			stderr=sc.sphinxStdErrFile).communicate()

	if builder == 'htmlhelp':
		hhpFile = os.path.join(os.path.join(targetFolder), sc.hhpName)
		command = sc.hhcExe + hhpFile
		if platform.system() == "Windows":
			p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=None,
				stderr=sc.sphinxStdErrFile, startupinfo=startupinfo).communicate()
		else:
			p = subprocess.Popen(commandArgs, stdin=subprocess.PIPE, stdout=None,
				stderr=sc.sphinxStdErrFile).communicate()

start = time.time()

args = sys.argv[1:]

if not args:
	builder = 'html'
	rebuildall = False
else:
	if len(args) != 2:
		print "you have to supply two args"
		print "e.g. 'html True' to use the html builder and force a full rebuild"
		sys.exit(2)
	else:
		if args[0] in sc.validBuilders:
			builder = args[0]
		else:
			print "builder %s is not valid" % args[0]
			sys.exit(2)
		if args[1].lower() == 'true':
			rebuildall = True
		else:
			rebuildall = False

# hack for Sphinx, clear out build/_images folder not to duplicate stuff
targetFolder = os.path.join(os.path.join(sc.baseFolder, 'build'), builder)
imgFolder = os.path.join(targetFolder, '_images')
if os.path.isdir(imgFolder):
    print "remove from build folder: %s" % imgFolder
    shutil.rmtree(imgFolder)


# build
MakeSphinx(builder, rebuildall)


# walk the tree to change files to writable
svnFolder = os.path.join(targetFolder, '_static\\macWidgets\\.svn')
if os.path.isdir(svnFolder):
    print "remove from build folder: %s" % svnFolder
    for top, dirs, files in os.walk(svnFolder):
        for item in files:
            os.chmod(os.path.join(top, item), stat.S_IWRITE)
    shutil.rmtree(svnFolder)
svnFolder = os.path.join(targetFolder, '_static\\winWidgets\\.svn')
if os.path.isdir(svnFolder):
    print "remove from build folder: %s" % svnFolder
    for top, dirs, files in os.walk(svnFolder):
        for item in files:
            os.chmod(os.path.join(top, item), stat.S_IWRITE)
    shutil.rmtree(svnFolder)
svnFolder = os.path.join(targetFolder, '_static\\nixWidgets\\.svn')
if os.path.isdir(svnFolder):
    print "remove from build folder: %s" % svnFolder
    for top, dirs, files in os.walk(svnFolder):
        for item in files:
            os.chmod(os.path.join(top, item), stat.S_IWRITE)
    shutil.rmtree(svnFolder)

current = time.time()
h, m, s = FractSec(int(current - start))

sc.sphinxStdErrFile.close()

# check for errors
errF = open(sc.sStdErr, 'r')
anyErr = errF.read()
if anyErr:
    print "\nThere were errors during the documentation generation, check: %s" % sc.sStdErr
else:
    print "\nDabo Documentation Sphinx build '%s' is finished. Elapsed time %02d:%02d:%02d" % (builder, h, m, s)
