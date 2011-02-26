# -*- coding: utf-8 -*-#

import os
import platform

# review and update as needed

# folder where .rst files will be stored
baseFolder = os.getcwd()
docFolder = os.path.join(baseFolder, "source")
# used to generate files, only changed and new ones will be copied to docFolder
# this speeds up the Sphinx build
rstTempFolder = os.path.join(baseFolder, "tempsource")
folderToDoc = os.path.join(baseFolder, "../dabo")

if platform.system() == "Windows":
	sphinxBuildCmd = "C:\\Python26\\Scripts\\sphinx-build.exe"
	# this is needed for the Sphinx Inheritance diagrams
	graphVizDot = ' -D graphviz_dot="C:\\Program Files (x86)\\Graphviz2.26.3\\bin\\dot.exe" '
	# is not tested yet
	hhcExe = "C:\Program Files (x86)\HTML Help Workshop\hhc.exe "

else:
	# needs to be adapted
	sphinxBuildCmd = "C:\\Python26\\Scripts\\sphinx-build.exe"
	graphVizDot = ' -D graphviz_dot="C:\\Program Files (x86)\\Graphviz2.26.3\\bin\\dot.exe" '
	hhcExe = "C:\Program Files (x86)\HTML Help Workshop\hhc.exe "


sStdErr = os.path.join(baseFolder, "sphinxstderr.txt")
sphinxStdErrStr = " -w %s " % sStdErr
sphinxStdErrFile = open(sStdErr, 'w')

# supported builders
normalHtml = "html"
helpHtml = "htmlhelp"
pdfDoc = "pdf" # doesn't work yet

validBuilders = [normalHtml, helpHtml]

# match entry in conf.py for htmlhelp_basename
hhpName = "dabo.hhp"


