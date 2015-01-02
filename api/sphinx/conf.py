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
#folderToDoc = r"c:\dev\dabo\dabo" # windows
folderToDoc = r"/home/ed/projects/dabo/dabo" # nix

if platform.system() == "Windows":
	sphinxBuildCmd = "C:\\Python26\\Scripts\\sphinx-build.exe" # windows
	# this is needed for the Sphinx Inheritance diagrams
	graphVizDot = 'graphviz_dot="C:\\Program Files (x86)\\Graphviz2.26.3\\bin\\dot.exe" '
	# is not tested yet
	hhcExe = "C:\Program Files (x86)\HTML Help Workshop\hhc.exe "

else:
	# needs to be adapted
	sphinxBuildCmd = r"/usr/local/bin/sphinx-build"
	graphVizDot = 'graphviz_dot=/usr/bin/dot'
	hhcExe = None # not applicable on non Windows

#graphviz_dot = "/usr/bin/dot"
sStdErr = os.path.join(baseFolder, "sphinxstderr.txt")
sphinxStdErrFile = open(sStdErr, 'a')

# supported builders
normalHtml = "html"
helpHtml = "htmlhelp"
singleHtml = "singlehtml"
pdfDoc = "pdf" # doesn't work yet

validBuilders = [normalHtml, helpHtml, singleHtml, pdfDoc]

# match entry in conf.py for htmlhelp_basename
hhpName = "dabo.hhp"

# Build extensions
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.inheritance_diagram',
]
