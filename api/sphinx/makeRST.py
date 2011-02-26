# -*- coding: utf-8 -*-#

import os
import sys

# force it
reload(sys)
sys.setdefaultencoding('utf-8')
del sys.setdefaultencoding

#import traceback
import subprocess

import glob
import inspect
import operator

#import wx
import datetime
import shutil
import re
import time
import filecmp

CROSS                   = 'Cross'
ROUNDED                 = 'Rounded'
SQUARE                  = 'Square'

CORNERS                 = [ROUNDED, SQUARE, CROSS]
CORNER_ID               = 'rounded_corner_r%d_f%d'
CROSS_POS               = (CROSS, CROSS, CROSS, CROSS)
ROUNDED_POS             = (ROUNDED, ROUNDED, ROUNDED, ROUNDED)
ROUNDED_RECTANGLE_ID    = 'rounded_rectangle_r%d_f%d_s%s_p%s'

MAXWIDTH = 120
BACKCOLOUR = (255, 255, 255, 255)

# get config stuff
from config import *

# needed for issubclass check
import dabo
# needed for describeDaboEvents
from dabo import dEvents

# use "en" for doc
dabo.dLocalize.setLanguage("en")

pictureIndex = {}

topLayer = "dabo"

subPackages = ["biz", "db", "lib", "ui"]

subSubPackages = {'lib': ["autosuper", "datanav"],
				  'ui': ["dialogs", "uiwx"]
				 }

# redefine the ui stuff
daboHack = ["dabo.ui.uiwx", "dabo.ui"]

# following cause import errors if I redefine them as e.g. dabo.ui.alignmentMixin
daboHackExceptions = ["dabo.ui.uiwx.alignmentMixin",
					  "dabo.ui.uiwx.dBaseMenuBar",
					  "dabo.ui.uiwx.dCalendar",
					  "dabo.ui.uiwx.dDateTextBox",
					  "dabo.ui.uiwx.dEditor",
					  "dabo.ui.uiwx.dFileDialog",
					  "dabo.ui.uiwx.dForm",
					  "dabo.ui.uiwx.dFormMain",
					  "dabo.ui.uiwx.dGrid",
					  "dabo.ui.uiwx.gridRenderers",
					  "dabo.ui.uiwx.dImageMixin",
					  "dabo.ui.uiwx.dLinePlot",
					  "dabo.ui.uiwx.dMessageBox",
					  "dabo.ui.uiwx.dPageFrame",
					  "dabo.ui.uiwx.dPageFrameNoTabs",
					  "dabo.ui.uiwx.dPemMixin",
					  "dabo.ui.uiwx.dProgressDialog",
					  "dabo.ui.uiwx.dRichTextBox",
					  "dabo.ui.uiwx.dSplitter",
					  "dabo.ui.uiwx.dTextBoxMixin",
					  "dabo.ui.uiwx.dTreeView",
					  "dabo.ui.uiwx.uiApp.SplashScreen",
					  "dabo.ui.uiwx.uiApp",
					  ]

# TODO: to be reviewed if there is no cleaner way of doing this
daboHackForLinks = {"EventMixin": ".lib.eventMixin.",
					"dPemMixin": ".ui.uiwx.",
					"dPemMixinBase": ".ui.",
					"PropertyHelperMixin": ".lib.",
					"dScrollPanel": ".ui.dPanel.",
					"dDateTextBox": ".ui.uiwx.",
					"dFormMixin": ".ui.",
					"dDataControlMixin": ".ui.",
					"dNode": ".ui.dTreeView.",
					"testNode": ".ui.uiwx.",
					"dControlMixin": ".ui.",
					}

# no links for "inherited from" for the following, also this should be handled by getPropertyList
# also used for methods, checks for the module name only
noInheritLink = ["wx._core", "wx._windows", "wx._controls", 
				 "wx.richtext", "wx.lib.pdfwin",
				 "wx.grid", 
				 "wx.html", "wx.lib.plot",
				 "simplejson.decoder", "wx.glcanvas",
				 "wx.gizmos", "wx._core",
				 "wx.lib.mixins.listctrl",
				 "wx.lib.masked.textctrl", 
				 "wx.lib.pdfwin","wx._misc",
				 "wx.lib.buttons",
				 "wx.calendar", "wx.stc",
				 "wx.aui", "wx.media",
				 "wx.lib.platebtn",
				 ]

noInheritLinkDabo = ["dabo.ui.uiwx.dPanel._BasePanelMixin",
					 "dabo.ui.uiwx.dMenuItem._AbstractExtendedMenuItem",]

# used to generate Index
subPackagesMods = ["dabo_module", "biz_module", "db_module", "lib_module"]

# don't create any TOC with glob for these
noTOCforMods = ["dabo.dConstants", "dabo.settings", "dabo.ui.concordance",
				"dabo.ui.uicurses", "dabo.biz.__init__", "dabo.lib.autosuper.__init__",
				"dabo.lib.datanav.__init__", "dabo.ui.dialogs.__init__"]

# define classes which should use autoclass + members
# otherwise we use getPropertyList, getMethodList and getEventList
docMembers = ["EventMixin", "EasyDialogBuilder", "autosuper", "SplashScreen"]

# classes which cause duplicate index entries
dupNoindex = ["Rect", "Rectangle", "autosuper", "lbl", "txt"]

# following can't be linked at the moment
noSuClassLink = ["dabo.db.dConnection.DaboCursor", "dabo.lib.autosuper.autosuper.autosuper", 
				 "wx._controls.StaticBitmap", "wx._controls.BitmapButton",
				 "wx._controls.StaticBox", "wx._controls.Button",
				 "wx._controls.CheckBox", "wx._controls.CheckListBox",
				 "wx._controls.ComboBox", "wx._controls.Choice",
				 "wx._controls.TextCtrl", "wx._controls.Gauge",
				 "wx._controls.StaticBitmap", "wx._controls.StaticText",
				 "wx._controls.StaticLine", "wx._controls.ListBox",
				 "wx._controls.ListCtrl", "wx._controls.SearchCtrl",
				 "wx._controls.Slider", "wx._controls.TextCtrl",
				 "wx._controls.ToolBar", "wx._controls.Notebook",
				 "wx._controls.Listbook", "wx._controls.Choicebook",
				 "wx._controls.Toolbook", "wx._controls.TreeCtrl",
				 "wx._windows.ColourDialog", "wx._windows.Dialog",
				 "wx._windows.FontDialog", "wx._windows.Panel",
				 "wx._windows.ScrolledWindow", "wx._windows.StatusBar",
				 "wx._windows.Printout", "wx._windows.FileDialog",
				 "wx._windows.DirDialog", "wx._windows.Frame",
				 "wx._windows.MiniFrame", "wx._windows.MessageDialog",
				 "wx._windows.SplitterWindow", "wx.richtext.RichTextCtrl",
				 "wx.grid.PyGridCellRenderer", "wx.grid.GridCellChoiceEditor",
				 "wx.grid.Grid", "wx.grid.PyGridTableBase",
				 "wx.html.HtmlWindow", "wx.lib.plot.PlotCanvas",
				 "simplejson.decoder.JSONDecoder", "simplejson.encoder.JSONEncoder", 
				 "wx.glcanvas.GLCanvas",
				 "wx.gizmos.EditableListBox", "wx._core.GridBagSizer",
				 "wx.lib.mixins.listctrl.ListCtrlAutoWidthMixin",
				 "wx.lib.masked.textctrl.TextCtrl", "wx.lib.plot.PlotCanvas",
				 "wx._core.app", "wx._core.Menu",
				 "wx._core.MenuBar", "wx._core.MenuItem",
				 "wx.lib.pdfwin.PDFWindow", "wx._core.BoxSizer",
				 "wx._core.Control", "wx._misc.Timer",
				 "wx.lib.buttons.GenBitmapTextToggleButton",
				 "wx.calendar.CalendarCtrl", "wx.stc.StyledTextCtrl",
				 "wx.aui.AuiNotebook", "wx._core.PyEvent",
				 "wx.tools.Editra.src.extern.flatnotebook.FlatNotebook",
				 "threading.Thread", "wx.media.MediaCtrl",
				 "dabo.ui.uiwx.dPanel._BasePanelMixin",
				 "dabo.ui.uiwx.dMenuItem._AbstractExtendedMenuItem",
				 "wx.lib.platebtn.PlateButton",
				 "dabo.ui.dBorderSizer.TestForm",
				 "dabo.ui.dPageFrameNoTabs.TestForm",
				 
				 "wx.lib.agw.aui",
				 "wx.lib.agw.FlatNotebook",
				 "wx.lib.agw.hyperlink.HyperLinkCtrl",
				 "wx.lib.agw.foldpanelbar.FoldPanelItem",
				 "wx.lib.agw.foldpanelbar.FoldPanelBar",
				 			 
				 ]


toRemove = ["__version__.py", "setup.py", "test.py"]

for pkg in subPackages:
	toRemove.append(pkg + "\\__init__.py")

for pkg in subSubPackages:
	for sub in subSubPackages[pkg]:
		toRemove.append(pkg + "\\" + sub + "\\__init__.py")

allPackages = []
allPackages.append("dabo.dabo")
for pkg in subPackages:
	allPackages.append("dabo." + pkg)
for pkg in subSubPackages:
	for sub in subSubPackages[pkg]:
		allPackages.append("dabo." + pkg + "." + sub)

# they cause getattr and similar error in Sphinx
excludedClasses = ["modglob", "connHandler", "FuncProfile", "FuncSource", "HotShotFuncCoverage",
				   "HotShotFuncProfile", "TraceFuncCoverage", "PageCountCanvas",
				   "specHandler", "Event", "TestForm", "Rect",
					
				   "__builtin__",
					]

# TODO: the Dabo ones cause import errors, i.e. probably something to do with namespace, just exclude them for now
# TODO: should this be full names, e.g. dabo.ui.uiwx.dPageFrame.onPageChanged?
excludedFunctions = ["PageFrame", "onPageChanged", "readonly", "main", 
					 "autoCreateTables", "setupAutoBiz", "resetHTML",
					 "textChangeHandler",
					 
					 "GetTranslation", "_gdi"]

excludedIcons = ["info.png", "note.png", "seealso.png", "todo.png", "warning.png", "navigation.png"]

# used in postProcess, not sure that we still have a use for it
replaces = {}

functionSummary = """
|method_summary| Function Summary
=================================

"""

classSummary = """
|class_summary| Class Summary
=============================

"""

DABO_modules = """
Module Summary
==============

.. toctree::
   :maxdepth: 1

   dabo.dApp_module
   dabo.dBug_module
   dabo.dColors_module
   dabo.dConstants_module
   dabo.dEvents_module
   dabo.dException_module
   dabo.dLocalize_module
   dabo.dObject_module
   dabo.dPref_module
   dabo.dReportWriter_module
   dabo.dSecurityManager_module
   dabo.dUserSettingProvider_module
   dabo.settings_module
   dabo.__init___module

"""

MAIN_modules = """
Module Summary
==============

.. toctree::
   :glob:
   :maxdepth: 1

"""

OTHER_TocTree = """
Module Summary
==============

.. toctree::
   :glob:
   :maxdepth: 1

%s

"""

classImage = """
|appearance| Control Appearance
===============================

.. figure:: _static/%s
   :alt: %s
   :figclass: floatcenter
   :align: center

   **%s**


"""

autosummary = """
.. autosummary::
   :nosignatures:

%s

"""

imagesLinks = """
.. include:: _static/headings.txt

"""

genindex = """
This is the master index for **Dabo - the desktop framework** (**Dabo**).

"""

thesummary = """
|method_summary| Methods Summary
================================

"""


knownSubs = """
|subclasses| Known Subclasses
=============================

%s

"""

knownSups = """
|supclasses| Known Superclasses
===============================

%s

"""

inheritance = """
|hierarchy| Inheritance Diagram
===============================

Inheritance diagram for: **%s**

.. inheritance-diagram:: %s
   :parts: 1

%s

%s

%s

%s

%s

|API| Class API
===============

"""

inheritanceDabo = """
|hierarchy| Inheritance Diagram
===============================

Inheritance diagram for: **%s**

.. inheritance-diagram:: %s

"""

noInheritance = """

%s

%s

%s

%s

%s

|API| Class API
===============

"""


htmlLayout = """
{% extends "!layout.html" %}

{%- block relbaritems %}
  <li>{{ title }}</li>
{% endblock %}

{% block rootrellink %}
				<li><img src="_static/dabo_small.png" alt="" style="vertical-align: middle; margin-top: 7px"/></li>
				<li><a href="index.html" style="color: rgb(238, 152, 22); hover: rgb(53, 95, 124);">Introduction</a> |&nbsp;</li>
				<li><a href="search.html" style="color: rgb(238, 152, 22); hover: rgb(53, 95, 124);">Search</a> |&nbsp;</li>
				<li><a href="gallery.html" style="color: rgb(238, 152, 22); hover: rgb(53, 95, 124);">Gallery</a> |&nbsp;</li>
				<li><a href="general_index.html" style="color: rgb(238, 152, 22); hover: rgb(53, 95, 124);">Contents</a>&raquo;</li>
{% endblock %}

{% block header %}
<div style="background-color: white; text-align: left; padding: 10px 10px 15px 15px">
<img src="{{ pathto("_static/dabo_logo.png", 1) }}" alt="Dabo Logo" />
</div>
{% endblock %}
"""

otherLayout = """
{% extends "!layout.html" %}

{%- block relbaritems %}
  <li>{{ title }}</li>
{% endblock %}

{% block rootrellink %}
				<li><img src="_static/dabo_small.png" alt="" style="vertical-align: middle; margin-top: 7px"/></li>
				<li><a href="index.html" style="color: rgb(238, 152, 22); hover: rgb(53, 95, 124);">Home</a> |&nbsp;</li>
				<li><a href="gallery.html" style="color: rgb(238, 152, 22); hover: rgb(53, 95, 124);">Gallery</a> |&nbsp;</li>
				<li><a href="general_index.html" style="color: rgb(238, 152, 22); hover: rgb(53, 95, 124);">Contents</a>&raquo;</li>
{% endblock %}

{% block header %}
<div style="background-color: white; text-align: left; padding: 10px 10px 15px 15px">
<img src="{{ pathto("_static/dabo_logo.png", 1) }}" alt="Dabo Logo" />
</div>
{% endblock %}
"""

rawhtmlfull = """

.. raw:: html

		<div class="panel">
				<p><img src="_static/dabo_small.png" alt="" style="vertical-align: middle; margin-right: 10px"/>
				<a style="color: rgb(255, 255, 255); font-size: x-large;"><b>Dabo</b></p>

				<ul class="simple" style="margin-left: 0; padding-left: 0;">
%s
				</ul>
		</div>

		<a class="trigger" href="#">Tree</a>

		<script type="text/javascript">
		$(document).ready(function(){
				$(".trigger").click(function(){
						$(".panel").toggle("fast");
						$(this).toggleClass("active");
						return false;
				});
		});
		</script>

"""

rawhtmlsingle = """            <li><a class="reference internal" href="%s"><em><b>%s</b></em></a></li>"""

svnrevisions = """
|svn_main| SVN Revisions
========================

A graphical representation of the SVN commits in the last year.

Click on any date in the picture to
jump to that particular revision page, containing information about committers, log
messages and SVN diffs.


%s


"""

os.chdir(os.path.join(docFolder, "_static"))

fullImages = glob.glob("*.png")# + glob.glob("*.jpg")
kImages = [os.path.splitext(img)[0] for img in fullImages]

os.chdir(baseFolder)

moduleauthor = "\n\n.. moduleauthor:: Dabo community <dabo-users@leafe.com>\n\n\n\n"

pattern = re.compile(r'{(.*?)}', re.DOTALL)


def bylength(word1, word2):

	return len(word2) - len(word1)


def replace_epydoc_links(name, obj, line):

	matches = pattern.findall(line)
	matches.sort(cmp=bylength)

	classes = lastMethods["class"]
	newMatches = matches[:]

	for m in matches:
		newM = "L{%s}"%m
		for kls, dummy in classes:
			if kls.endswith(m):
				line = line.replace(newM, ":class:`~%s`"%kls)
				newMatches.remove(m)
				break

	matches = newMatches[:]
	methods = lastMethods["method"]

	for m in matches:
		newM = "L{%s}"%m
		for kls, method in methods:
			if method.endswith(m):
				line = line.replace(newM, ":meth:`~%s`"%method)
				newMatches.remove(m)
				break

	if newMatches:
		print "\n==================================================="
		print "UNCONVERTED LINKS IN %s:"%name
		print "===================================================", "\n"
		for m in newMatches:
			print " "*4, m

		print "\n\n"

	return line


def MangleDocs(myname, docs, strip=True, replacetabs=True):

	if docs:
		if replacetabs:
			docs = docs.replace("\t", "    ")
		lines = docs.split("\n")
	else:
		lines = ['', '', '']
	twopoints = False
	empty = 0
	tostrip = True
	addspace = 0

	for i, line in enumerate(lines):

		if not line.strip():
			empty += 1
		else:
			empty = 0

		if empty == 2:
			tostrip = True
			empty = 0
			addspace = 0

		if strip and tostrip:
			lines[i] = " "*addspace + lines[i].strip()

		if "::" in line:
			tostrip = False

		if ":note:" in line:
			addspace = 1

	for i, line in enumerate(lines):
		if "L{" in line:
			lines[i] = replace_epydoc_links(myname, None, line)

	stylesDone, extraDone = False, False

	for i, line in enumerate(lines):
		found = False

		if line.startswith("Description"):
			line = "|description| " + line
			lines[i] = line
			found = True

		elif (line.startswith("Usage") or line.startswith("Base Functionalities")) and "::" not in line:
			line = "|usage| " + line
			lines[i] = line
			found = True

		elif line.startswith("Methods and Settings"):
			line = "|settings| " + line
			lines[i] = line
			found = True

		elif line.startswith("Window Styles") and not stylesDone:
			line = "|styles| " + line
			lines[i] = line
			found = True
			stylesDone = True

		elif line.startswith("Window Extra Styles") and not extraDone:
			line = "|extra_styles| " + line
			lines[i] = line
			found = True
			extraDone = True

		elif line.startswith("License "):
			line = "|license| " + line
			lines[i] = line
			found = True

		elif line.startswith("Supported Platform"):
			line = "|platforms| " + line
			lines[i] = line
			found = True

		elif line.startswith("Events"):
			line = "|events| " + line
			lines[i] = line
			found = True

		elif line.startswith("Appearance"):
			line = "|appearance| " + line
			lines[i] = line
			found = True

		elif line.startswith("Example Usage"):
			line = "|usage| " + line
			lines[i] = line
			found = True

		elif line.startswith("See Also"):
			line = "|link| " + line
			lines[i] = line
			found = True

		elif line.startswith("TODOs"):
			line = "|todos| " + line
			lines[i] = line
			found = True

		elif line.startswith("Vision "):
			line = "|vision| " + line
			lines[i] = line
			found = True

		elif line.startswith("What's New"):
			line = "|whatsnew| " + line
			lines[i] = line
			found = True

		elif line.startswith("Layers, Rows "):
			line = "|layers| " + line
			lines[i] = line
			found = True

		elif line.startswith("Backward Incompatibilities"):
			line = "|backward| " + line
			lines[i] = line
			found = True

		if found:
			lines[i+1] = lines[i+1].strip() + "===================\n"
			
	return "\n".join(lines)


def WriteSphinxFile(name, docs, hasCross=None, moduleData=None, raw=""):

	# TODO: is this to agressive
	if "_" in name and not "__init__" in name:
		return

	cross = ""
	if daboHack[0] in name and not name in daboHackExceptions:
		# some links use the "non" hacked name, e.g. dabo.ui.uiwx,
		# therefore we need an index for it
		cross = ".. _%s:\n\n" % name
		name = name.replace(daboHack[0], daboHack[1])
		# and the hacked index
		cross = ".. _%s:\n\n" % name
	else:
		# an index for each module
		cross = ".. _%s:\n\n" % name
	if name in daboHackExceptions:
		# we can't change the name, but we need an index with changed 
		# name for links (e.g. superclasses)
		cross += ".. _%s:\n\n" % name.replace(daboHack[0], daboHack[1])

	fileName = name + "_module.rst"

	currentmodule = ""

	if moduleData:
		if daboHack[0] in name and not name in daboHackExceptions:
			name = daboHack[1]
			noIndex = True
		module = ".. module:: %s\n\n" % name
		currentName = moduleData.__name__
	else:
		if daboHack[0] in name and not name in daboHackExceptions:
			name = daboHack[0]
			noIndex = True
		module = ".. module:: %s\n\n" % name
		currentName = name

	icon = "|doc_title| "

	title = name.split(".")[-1:][0]
	if name in allPackages:
		title += " package"
	else:
		title += " module"

	lenSpace = (len(title) + len(icon) + 5)

	title = "="*lenSpace + "\n%s **"%icon + title + "**\n" + "="*lenSpace + "\n\n"
	highlight = "|\n\n.. highlight:: python\n\n"

	text = module + currentmodule + cross + title + highlight +\
									MangleDocs(name, docs, False) + moduleauthor
	tt3 = ""

	# exclude "_" privat stuff in describe_module
	functions, klasses = describe_module(moduleData)

	if functions or klasses:
		text += "\n\n"

	if functions:
		text += functionSummary + "\n"
		for fun, obj in functions:
			text += "* :meth:`~%s`\n" % (obj.__module__ + "." + obj.__name__)

		if klasses:
			text += "\n\n"

	tclass = []
	if klasses:
		text += classSummary + "\n"
		for kls, obj in klasses:
			# included in tocTree below
			#text += "* :ref:`%s`\n" % (obj.__module__ + "." + kls)
			tclass.append(obj.__module__ + "." + kls)

	glb = glob.glob(name + "*.rst")
	glb.sort(key=str.lower)
	glb = [gl[0:-4] for gl in glb if "_module.rst" not in gl]
	glb2 = []
	for gl in glb:
		if ".__" in gl or "__" not in gl:
			glb2.append(gl)

	strs = ""
	glb2.sort(key=str.lower)
	for gl in glb2:
		strs += "   %s\n" % gl

	if name == "dabo.dabo":
		text += DABO_modules
	else:
		if strs:
			text += OTHER_TocTree % strs
		else:
			if name in noTOCforMods:
				# no toc for these in the _module, there are no sub-mods for them
				text += "\n"
			else:
				text += OTHER_TocTree % ("   " + name + "*")

	fid = open(fileName, "wt")
	fid.write(imagesLinks + text + raw)
	fid.close()

	tfun = ""

	if functions:
		fun, obj = functions[0]
		if daboHack[0] in obj.__module__:
			objName = obj.__module__.replace(daboHack[0], daboHack[1])
		else:
			objName = obj.__module__
		funName = "%s.rst" % (objName)
		fid = open(funName, "wt")
		text = ".. module:: %s\n\n" % obj.__module__
		# an index for each function
		text += ".. _%s:\n\n" % (obj.__module__+ "._Functions")

		tfun = obj.__module__ + "._Functions"

		icon = "|doc_title| "

		# TODO: just use tail for title of doc?
		fixName = obj.__module__.split(".")[-1:][0]
		leno = len(fixName) + 15 + len(icon)
		text += "="*leno + "\n**" + fixName + "** functions\n" + "="*leno + "\n\n"

		text += "This is the description of standalone Python functions in the **%s** module.\n\n" % obj.__module__
		text += "|method_summary| Functions Summary\n" + "="*34 + "\n\n"
		summary = ""
		for fun, obj in functions:
			summary += "   %s\n"%fun

		text += autosummary%summary + "\n"
		text += "|API| Functions API\n" + "="*19 + "\n\n\n"

		for fun, obj in functions:
			text += describe_func(obj)

		fid.write(imagesLinks + text + raw)
		fid.close()

	if klasses:
		for kls, obj in klasses:
			if daboHack[0] in obj.__module__ and not obj.__module__ in daboHackExceptions:
				kModName = obj.__module__.replace(daboHack[0], daboHack[1])
			else:
				kModName = obj.__module__
			klsName = "%s.rst" % (kModName + "." + kls)
			fid = open(klsName, "wt")
			text = describeDaboKlass(obj, kls, klsName)
			fid.write(imagesLinks + text + raw)
			fid.close()


def MakeInitDocs(name, raw):
	os.chdir(rstTempFolder)

	# prefix topLayer
	tag = topLayer + "." + name
	docs = __import__(name).__doc__

	# do the dabo_module.rst
	WriteSphinxFile(tag, docs, raw=raw)

	# do the subPackage_module.rst
	for subP in subPackages:
		# prefix topLayer
		tag = topLayer + "." + subP
		docs = __import__(tag, fromlist=subP).__doc__
		WriteSphinxFile(tag, docs, raw=raw)

		if subSubPackages.has_key(subP):
			for subSubP in subSubPackages[subP]:
				# prefix topLayer
				tag = topLayer + "." + subP + "." + subSubP
				#following does not work for subsubs
				#docs = __import__(tag).__doc__
				docs = ''
				WriteSphinxFile(tag, docs, raw=raw)

def MakeModuleDocs(folder=None, raw=""):
	"""Get the .py files from the folder and generate a .rst file for each one found,
	except for the ones defined in "toRemove"
	"""
	os.chdir(folderToDoc)
	if folder is None:
		otherPython = glob.glob("*.py")
	else:
		pFolder = folder.replace(".", os.path.sep)
		otherPython = glob.glob(pFolder + "/*.py")

	for item in toRemove:
		if folder:
			pFolder = folder + "."
			pFolder = pFolder.replace(".", os.path.sep)
			cItem = pFolder + item
		else:
			cItem = item
		if cItem in otherPython:
			otherPython.remove(cItem)

	os.chdir(rstTempFolder)

	for item in otherPython:
		moduleName = topLayer + os.path.sep + os.path.splitext(item)[0]
		hasPoint = os.path.sep in moduleName
		if hasPoint:
			mainName, secondaryName = os.path.split(moduleName)
			moduleName = moduleName.replace(os.path.sep, ".")
			moduleData = __import__(moduleName, fromlist=[secondaryName])
		else:
			moduleData = __import__(moduleName)

		docs = moduleData.__doc__
		realName = None
		for objects in dir(moduleData):
			if objects.lower() == moduleName:
				realName = objects

		hasCross = None
		if realName is None:

			if "." in moduleName:
				name = moduleName[moduleName.index(".")+1:]
			else:
				name = moduleName

			realName = moduleName
			hasCross = name

		WriteSphinxFile(moduleName, docs, hasCross, moduleData, raw=raw)

def describe_builtin(obj):
	""" Describe a builtin function """

	# Built-in functions cannot be inspected by
	# inspect.getargspec. We have to try and parse
	# the __doc__ attribute of the function.
	docstr = obj.__doc__
	args = ''

	if docstr:
		items = docstr.split('\n')
		if items:
			func_descr = items[0]
			s = func_descr.replace(obj.__name__,'')
			idx1 = s.find('(')
			idx2 = s.find(')',idx1)
			if idx1 != -1 and idx2 != -1 and (idx2>idx1+1):
				args = s[idx1+1:idx2]

def describeDaboMethods(kls, methods):
	""" Describe the methods object passed as argument."""

	inheritedMethods = ""
	ownMethods = ""
	for method in methods:
		isInherited = False
		strs = ""
	
		if type(kls) == type:
			m = None
			definedIn = None
			for o in kls.__mro__:
				try:
					m = o.__dict__[method]
					definedIn = o
				except KeyError:
					continue
				break
			if m is None:
				return ""
		else:
			m = getattr(kls, method)
			definedIn = kls

		if definedIn != kls:
			isInherited = True
	
		args = inspect.getargspec(m)
		args = inspect.formatargspec(args[0], args[1], args[2], args[3])
	
		rArgs = args.replace("*args", "\*args").replace("**kwargs", "\**kwargs").replace("**", "\**").replace("*", "\*")
		# have to use kls info to prevent duplicate defintion, because of Dabo name mangling
		strs += ".. function:: " + kls.__module__ + "." + kls.__name__ + "." + method + rArgs
		if isInherited:
			strs += "\n   :noindex:\n"
		
		strs += "\n\n"
		if m.__doc__ is None:
			strs += "\n"
		else:
			doc = ""
			for line in m.__doc__.splitlines():
				doc += "   " + line.replace("\t", "", 2).replace("\t", "    ") + "\n"
			strs += doc + "\n\n"
	
		if isInherited:
			if definedIn.__module__ in noInheritLink:
				strs += "Inherited from: '%s - can not provide a link\n" % (definedIn.__module__ + "." + definedIn.__name__)
			elif definedIn.__module__ + "." + definedIn.__name__ in noInheritLinkDabo:
				strs += "Inherited from: '%s - can not provide a link\n" % (definedIn.__module__ + "." + definedIn.__name__)
			else:
				if daboHackForLinks.has_key(definedIn.__name__):
					strs += "Inherited from: :ref:`%s`\n" % (topLayer + daboHackForLinks.get(definedIn.__name__) + definedIn.__name__)
				else:
					strs += "Inherited from: :ref:`%s`\n" % (definedIn.__module__ + "." + definedIn.__name__)
	
		strs += "\n-------\n\n"
		
		if isInherited:
			inheritedMethods += strs
		else:
			ownMethods += strs
	
	allStrs = ""
	if ownMethods:
		allStrs += "\nMethods\n"
		allStrs += "=======\n\n"
		allStrs += ownMethods
	if inheritedMethods:
		allStrs += "\nMethods - inherited\n"
		allStrs += "=====================\n\n"
		allStrs += inheritedMethods

	return allStrs

def describeDaboProperties(kls, props):
	""" Describe the properties object passed as argument."""

	inheritedProps = ""
	ownProps = ""

	for prop in props:
		isInherited = False
		strs = ""
		if prop[:9] == "[Dynamic]":
			prop = prop[9:]
		d = kls.getPropertyInfo(prop)
	
		strs += "**" + prop + "** " + "\n\n"
		if d["doc"] is None:
			strs += "\n"
		else:
			doc = ""
			for line in d["doc"].splitlines():
				doc += line.replace("\t", "", 2).replace("\t", "    ") + "\n"
			strs += doc + "\n\n"
	
		if d["definedIn"] != kls:
			definedIn = d["definedIn"]
			isInherited = True
			if definedIn.__module__ in noInheritLink:
				# we shouldn't get here, as we use getPropertyList with onlyDabo=True
				strs += "Inherited from: '%s - can not provide a link\n" % (definedIn.__module__ + "." + definedIn.__name__)
			elif definedIn.__module__ + "." + definedIn.__name__ in noInheritLinkDabo:
				strs += "Inherited from: '%s - can not provide a link\n" % (definedIn.__module__ + "." + definedIn.__name__)
			else:
				if daboHackForLinks.has_key(definedIn.__name__):
					strs += "Inherited from: :ref:`%s`\n" % (topLayer + daboHackForLinks.get(definedIn.__name__) + definedIn.__name__)
				else:
					strs += "Inherited from: :ref:`%s`\n" % (definedIn.__module__ + "." + definedIn.__name__)

		strs += "\n-------\n\n"
		
		if isInherited:
			inheritedProps += strs
		else:
			ownProps += strs

	allStrs = ""
	if ownProps:
		allStrs += "\nProperties\n"
		allStrs += "==========\n\n"
		allStrs += ownProps
	if inheritedProps:
		allStrs += "\nProperties - inherited\n"
		allStrs += "========================\n\n"
		allStrs += inheritedProps

	return allStrs

def describeDaboEvents(kls, events):
	""" Describe the event objects passed as argument."""

	allEvents = ""
	for event in events:
		strs = ""
		e = dEvents.__dict__[event]
	
		strs += "**" + event + "** " + "\n\n"
		if e.__doc__ is None:
			strs += "\n"
		else:
			doc = ""
			for line in e.__doc__.splitlines():
				doc += line.replace("\t", "", 1).replace("\t", "    ") + "\n"
			strs += doc + "\n\n"
	
		strs += "\n-------\n\n"

		allEvents += strs

	allStrs = ""
	if allEvents:
		allStrs += "\nEvents\n"
		allStrs += "=======\n\n"
		allStrs += allEvents

	return allStrs

def describe_func(obj, method=False, kls=""):
	"""
	Describe the function object passed as argument.
	If this is a method object, the second argument will
	be passed as True, kls is used to fix up the automethod something.__init__
	"""

	strs = ""

	if method:
		if obj.__name__ == "__init__":
			if kls:
				tmp = kls + "." + obj.__name__
			else:
				tmp = obj.__module__ + "." + obj.__name__
			strs += '   .. automethod:: %s\n' % tmp
			return strs
		else:
			return strs
	else:
		if obj.__name__ in excludedFunctions:
			return strs

	strs += '   .. autofunction:: %s' % (obj.__module__ + "." + obj.__name__)

	try:
		arginfo = inspect.getargspec(obj)
	except TypeError:
		return strs

	args = arginfo[0]
	argsvar = arginfo[1]
	input = []

	if args:
		if args[0] == 'self':
			args.pop(0)

		input = args
		defargs, defval = [], []

		if arginfo[3]:
			dl = len(arginfo[3])
			al = len(args)
			defargs = args[al-dl:al]
			defval = arginfo[3]

	strs += "("
	for indx, item in enumerate(input):
		if indx > 0:
			strs += ", "
		if item in defargs:
			index = defargs.index(item)
			strs += "%s=%s"%(item.strip(), repr(defval[index]).strip())
		else:
			strs += "%s"%item

	strs += ")\n"

	return strs

def describeDaboKlass(obj, klsinc, klsfilename):
	"""Describe the class object passed as argument,
	including its methods
	
	klsinc is just used to see if we need noindex
	"""

	noIndex = False
	if klsinc in dupNoindex:
		noIndex = True

	subclasses = ""
	superclasses = ""
	try:
		subs = obj.__subclasses__()
	except:
		subs = []

	sups = list(obj.__bases__)

	sortedSubClasses = []
	sortedSupClasses = []

	for item in sups:
		item = repr(item)
		sup = item.replace("<class ", "").replace(">", "")
		if sup.startswith("wx.") or sup.startswith("<type"):
			continue
		sortedSupClasses.append(sup.strip().replace('"', "").replace("'", ""))

	if subs:
		for s in subs:
			s = repr(s)
			start = s.index("'")
			end = s.rindex("'")
			cls = s[start+1:end]
			sortedSubClasses.append(cls)
		sortedSubClasses.sort()
		for cls in sortedSubClasses:
			if daboHack[0] in cls and cls not in daboHackExceptions:
				cls = cls.replace(daboHack[0], daboHack[1])
			if "._" in cls:
				# ingore all the privat classes which somehow got here
				continue
			else:
				if cls in noSuClassLink:
					subclasses += "* %s - can not provide a link\n" % cls
				else:
					subclasses += "* :ref:`%s`\n" % cls

		subclasses = knownSubs % subclasses

	if sortedSupClasses:
		sortedSupClasses.sort()
		for s in sortedSupClasses:
			if "wx.lib.agw." in s:
				# intersphinx is not yet working for this
##				cls = "<agw:%s>" % s.replace("wx.lib.agw.", "")
				cls = s
			else:
				if daboHack[0] in s and s not in daboHackExceptions:
					cls = s.replace(daboHack[0], daboHack[1])
				else:
					cls = s
			if "._" in cls:
				# ingore all the privat classes which somehow got here
				continue
			else:
				if cls in noSuClassLink:
					superclasses += "* %s - can not provide a link\n" % cls
				else:
					superclasses += "* :ref:`%s`\n" % cls

		superclasses = knownSups % superclasses

	name = obj.__module__
	if daboHack[0] in name and not name in daboHackExceptions:
		name = daboHack[1]
	strs = ".. module:: %s\n\n" % name

	if daboHack[0] in obj.__module__ and not obj.__module__ in daboHackExceptions:
		tmp = obj.__module__.replace(daboHack[0], daboHack[1])
		# an index for each name within the module, daboHack applied
		strs += ".. _%s:\n\n" % (tmp + "." + obj.__name__)
		# if source is in package, create another index
		if "__init__" in tmp:
			strs += ".. _%s:\n\n" % (tmp.replace(".__init__", "") + "." + obj.__name__)
	if obj.__module__ in daboHackExceptions:
		# we also need an index without daboHack for exceptions for links (e.g. superclasses)
		strs += ".. _%s:\n\n" % (obj.__module__.replace(daboHack[0], daboHack[1]) + "." + obj.__name__)

	# an index for each name within the module
	# if daboHack then this will create one with original name e.g. dabo.ui.uiwx
	strs += ".. _%s:\n\n" % (obj.__module__ + "." + obj.__name__)
	# if source is in package, create another index
	if "__init__" in obj.__module__:
		strs += ".. _%s:\n\n" % (obj.__module__.replace(".__init__", "") + "." + obj.__name__)

	icon = "|doc_title| "

	fixName = obj.__module__.split(".")[-1:][0] + "." + obj.__name__
	lenSpace = (len(fixName) + len(icon) + 13) # emphasize and class text

	strs += "="*lenSpace + "\n%s **"%icon + fixName + "** - class\n" + "="*lenSpace + "\n\n"

	if obj.__doc__:
		strs += MangleDocs(obj.__name__, obj.__doc__) + "\n\n"

	count = 0
	keys = obj.__dict__.keys()
	keys.sort()
	kls = obj

	if "__init__" in keys:
		keys.remove("__init__")
		keys.insert(0, "__init__")

	methodNames = []
	for name in keys:
		item = getattr(obj, name)
		if inspect.ismethod(item):
			methodNames.append((name, item))

	strs += "\n"

	if kls.__name__ in kImages:
		index = kImages.index(kls.__name__)
		img1, img2 = fullImages[index], kls.__name__
		hasPicture = classImage % (img1, img2, img2)
		pictureIndex[img2] = klsfilename.replace(".rst", ".html")
	else:
		hasPicture = ""

	if superclasses:
		strs += inheritanceDabo % (kls.__name__, kls.__name__)
		strs += superclasses

	if subclasses:
		strs += subclasses

	if hasPicture:
		strs += hasPicture

	# just get the class definition and doc, the rest we do manually
	strs += "\n|API| Class API\n"
	strs += "===============\n\n"

	if daboHack[0] in kls.__module__ and not kls.__module__ in daboHackExceptions:
		modName = daboHack[1]
	else:
		modName = kls.__module__
	
	if kls.__name__ in docMembers:
		strs += "\n.. autoclass:: %s" % (modName + "." + kls.__name__)
		if noIndex:
			strs += "\n   :noindex:"
		strs += "\n   :members:\n\n"
	else:
		strs += "\n.. autoclass:: %s" % (modName + "." + kls.__name__)
		if noIndex:
			strs += "\n   :noindex:"
		strs += "\n\n"

	# TODO: is this really only getting "__init__"
	for name, item in methodNames:
		strs += describe_func(item, True, modName + "." + kls.__name__)

	if hasattr(kls, "getPropertyList"):
		# as per Paul, only include Dabo's properties
		strs += describeDaboProperties(kls, kls.getPropertyList(refresh=True, onlyDabo=True))

	if hasattr(kls, "getEventList"):
		strs += describeDaboEvents(kls, kls.getEventList())

	if hasattr(kls, "getMethodList"):
		strs += describeDaboMethods(kls, kls.getMethodList(refresh=True))

	return strs

def describe_module(module):

	count = 0

	d = dir(module)
	d.sort()

	klasses, functions, methods = [], [], []

	for name in d:
		obj = getattr(module, name)
		if name == "_":
			continue
		if inspect.isclass(obj):
			if obj.__module__ in excludedClasses or name in excludedClasses:
				continue
			if obj.__module__ != module.__name__:
				continue
			# ignore "_", i.e. privat
			if name.startswith("_"):
				continue
			klasses.append((name, obj))
		elif inspect.isfunction(obj):
			if obj.__module__ != module.__name__:
				continue
			# ignore "_", i.e. privat
			if name.startswith("_"):
				continue
			if name in excludedFunctions:
				continue
			functions.append((name, obj))
		elif inspect.ismethod(obj):
			# ignore "_", i.e. privat
			if name.startswith("_"):
				continue
			methods.append((name, obj))
		elif inspect.isbuiltin(obj):
			describe_builtin(obj)

	klasses.sort(key=operator.itemgetter(0))
	functions.sort(key=operator.itemgetter(0))

	return functions, klasses

def AddPrettyTable(text, isModule, fileName):

	newtext = """<br>
<table border="1" class="docutils"> """
	newtext2 = """<br>
<table border="1" class="last docutils"> """

	text = text.replace('<table border="1" class="docutils">', newtext)

	text = text.replace('<table border="1" class="last docutils">', newtext2)

	othertext = """class="pretty-table"><caption>%s</caption>"""

	currentCaption = " "
	returnCaption = " "

	if isModule:
		thefile = os.path.split(fileName)[1]
		lines = text.split("\n")
		for indx, line in enumerate(lines):
			if 'class="docutils"' in line:
				lines[indx] = lines[indx].replace('class="docutils">', othertext%currentCaption)
				currentCaption = " "
			elif 'class="last docutils"' in line:
				lines[indx] = lines[indx].replace('class="last docutils">', othertext%returnCaption)
				returnCaption = " "

			elif "Window Styles" in line:
				currentCaption = "Window styles for <b>%s</b>"%thefile[0:-12]
			elif "Window Extra" in line:
				currentCaption = "Window extra styles for <b>%s</b>"%thefile[0:-12]
			elif "Events Processing" in line:
				currentCaption = "Events processing for <b>%s</b>"%thefile[0:-12]
			elif '<tt class="descname">' in line:
				start = line.index(">")
				end = line.index("</tt>")
				returnCaption = line[start+1:end]

		return "\n".join(lines)

	lines = text.split("\n")
	skip = False

	currentCaption = " "
	returnCaption = " "

	for indx, line in enumerate(lines):
		if "method-summary-" in line or "Table of Contents" in line:
			skip = True
		elif "</table>" in line:
			skip = False

		if " Code Statistics" in line:
			currentCaption = "Code statistics for <b>Dabo</b> (%s)"%datetime.datetime.now().strftime("%d-%B-%Y")
		elif "&#8211;" in line and "</em>" in line and "<em>" in line:
			em1, em2 = line.index("<em>"), line.index("</em>")
			parameter = line[em1+4:em2]
			currentCaption = "<b>%s</b> parameter settings"%parameter
		elif '<tt class="descname">' in line:
			start = line.index(">")
			end = line.index("</tt>")
			returnCaption = line[start+1:end]
			returnCaption = "Return values for <b>%s</b>"%returnCaption

		if not skip:
			if 'class="docutils">' in line:
				lines[indx] = lines[indx].replace('class="docutils">', othertext%currentCaption)
				currentCaption = " "
			elif 'class="last docutils"' in line:
				lines[indx] = lines[indx].replace('class="last docutils">', othertext%returnCaption)
				returnCaption = " "


	return "\n".join(lines)


def RemoveInheritanceTag(text):

	if "digraph " not in text:
		return text

	indx1 = text.index("digraph ")
	indx2 = text[indx1:].index("}")

	text = text[0:indx1] + "Inheritance diagram" + text[indx1+indx2+1:]

	return text


def DeleteSummaryHierarchy(text):

	newText = ""
	found = False
	todo = True

	for line in text.split("\n"):
		if 'style="width: 32px;" /> Methods Summary' in line:
			found = True
			newText += line + "\n"
			continue

		if not found:
			newText += line + "\n"
			continue

		if "</tbody>" in line:
			found = False
			newText += line + "\n"
			continue

		if "</tr>" in line:
			todo = True

		if '<span class="pre">' in line and todo:
			index = line.index('<span class="pre">') + len('<span class="pre">')
			newBlock = line[index:]
			if "." in newBlock:
				index2 = newBlock.rindex(".")+1
				newBlock2 = newBlock[index2:]
			else:
				newBlock2 = newBlock
			newText += line[0:index] + newBlock2
			todo = False
		else:
			newText += line + "\n"

	return newText


def RemovePanel(text):

	tt = text.split("\n")
	newText = []
	toContinue = False

	for line in tt:

		if toContinue:
			if '<a class="trigger" href="#">Tree</a>' in line:
				toContinue = False
				continue

		if line.startswith('"<script type="text/javascript">') and line.strip() == '<script type="text/javascript">':
			toContinue = True

		if not toContinue:
			newText.append(line)

	return "\n".join(newText)


def AddJS(text):

	tt = text.split("\n")
	newText = []

	for line in tt:
		newText.append(line)
		if "meta http-equiv" in line:
			newText.append('    <script type="text/javascript" src="_static/jquery.js"></script>')

	return "\n".join(newText)


def PostProcess(builder):

	os.chdir(baseFolder)
	folder = os.path.join(os.path.join(baseFolder, "build"), builder + '/%s')

	fileNames = glob.glob(folder % "*.html")

	for files in fileNames:

		if "2to3" in files:
			continue
		if "genindex" in files or "modindex" in files:
			continue

		fid = open(files, "rt")
		text = fid.read()
		fid.close()

		text = text.replace("doc-title-", "")
		text = text.replace("doc_title  ", "")
		text = text.replace("<em>doc_title ", "<em>")

		isModule = "_module" in files
		text = AddPrettyTable(text, isModule, files)

		if folder == helpHtml:
			text = AddJS(text)

		text = text.replace('&#8211; <p>', '&#8211; ')
		text = text.replace('<dl class="method">', '<br><hr />\n<dl class="method">')
		text = text.replace('<dl class="function">', '<br><hr />\n<dl class="function">')
		text = text.replace('<dl class="classmethod">', '<br><hr />\n<dl class="classmethod">')
		text = text.replace('<dl class="attribute">', '<br><hr />\n<dl class="attribute">')

		text = RemoveInheritanceTag(text)
		text = DeleteSummaryHierarchy(text)

		fid = open(files, "wt")
		fid.write(text)
		fid.close()

	fid = open(folder%"index.html", "rt")
	text = fid.read()
	fid.close()

	text = text.replace("module ", "")
	text = text.replace(" library", "")

	lines = text.split("\n")
	keys = replaces.keys()

	for indx, line in enumerate(lines):
		for key in keys:
			thekey = '<em>%s</em>' % key
			repl = '<em>%s</em>'
			if thekey in line:
				lines[indx] = lines[indx].replace(thekey, repl % replaces[key])
				break

		if 'src="_images/Stats.png"' in line:
			break

	text = "\n".join(lines)
	fid = open(folder % "index.html", "wt")
	fid.write(text)
	fid.close()

	topM = ["general_index", ] + subPackagesMods
	for f in topM:
		fileName = folder % f + ".html"
		if not os.path.isfile(fileName):
			continue

		fid = open(fileName, "rt")
		text = fid.read()
		fid.close()

		text = text.replace("<em>module ", "<em>")
		if "general_index" in f:
			text = text.replace(" library", "")

		fid = open(folder % f + ".html", "wt")
		fid.write(text)
		fid.close()


def MakeHTMLHelp(folder):

	print "\nGenerating CHM Help File..."
	htmlProject = folder % hhcName
	os.system("%s %s"%(hhcExe, htmlProject))
	print "CHM help file generated."

	source = folder % chmName
	dest = normalHtml % chmName
	shutil.copyfile(source, dest)


def MakeBackups():

	fileNames = glob.glob("_build/html/*.html")
	htmlFiles = glob.glob("_dummyHtml/*.html")

	for files in htmlFiles:
		os.remove(files)

	for files in fileNames:
		shutil.copyfile(files, "_dummyHtml/"+os.path.split(files)[1])


def WriteGeneralIndex():

	fid = open("general_index.rst", "wt")
	lastLen = 0
	fid.write(imagesLinks + "\n")
	fid.write("\n.. _daboindex:\n\n")
	fid.write("================================\n")
	fid.write("|doc_title| Master Index\n")
	fid.write("================================\n\n")
	fid.write(genindex)

	# not that great
	fid.write("\nPackage Index")
	fid.write("\n=============\n\n")
	fid.write(".. tocTree::\n")
	fid.write("   :maxdepth: 1\n\n")
	for item in allPackages:
		if daboHack[0] not in item:
			fid.write(("   %s_module\n" % item))
	fid.write("\n\n")
	
	# now do all the items within each package
	all = glob.glob(rstTempFolder + "\*.rst")
	
	dTop = []
	dBiz = []
	dLib = []
	dLibA = []
	dLibD = []
	dDb = []
	dDbx = []
	dUi = []
	dUix = []
	dUid = []
	
	for item in all:
		if "dabo.biz" in item and not "_module.rst" in item:
			dBiz.append(item)
		elif "dabo.db.db" in item and not "_module.rst" in item:
			dDb.append(item)
		elif "dabo.db" in item and not "_module.rst" in item:
			dDbx.append(item)
		elif "dabo.lib.autosuper" in item and not "_module.rst" in item:
			dLibA.append(item)
		elif "dabo.lib.datanav" in item and not "_module.rst" in item:
			dLibD.append(item)
		elif "dabo.lib" in item and not "_module.rst" in item:
			dLib.append(item)
		elif "dabo.ui.uiwx" in item and not "_module.rst" in item:
			dUix.append(item)
		elif "dabo.ui.dialogs" in item and not "_module.rst" in item:
			dUid.append(item)
		elif "dabo.ui" in item and not "_module.rst" in item:
			dUi.append(item)
		elif "index" in item and not "_module.rst" in item:
			pass
		elif not "_module.rst" in item:
			dTop.append(item)

	fid.write("Dabo\n")
	fid.write("====\n\n")
	fid.write(".. tocTree::\n")
	fid.write("   :maxdepth: 1\n\n")
	for item in dTop:
		fid.write("   %s\n" % os.path.split(item)[1].replace(".rst", ""))
	fid.write("\n\n")

	fid.write("Dabo - db\n")
	fid.write("=========\n\n")
	fid.write(".. tocTree::\n")
	fid.write("   :maxdepth: 1\n\n")
	for item in dDb:
		fid.write("   %s\n" % os.path.split(item)[1].replace(".rst", ""))
	for item in dDbx:
		fid.write("   %s\n" % os.path.split(item)[1].replace(".rst", ""))
	fid.write("\n\n")

	fid.write("Dabo - biz\n")
	fid.write("==========\n\n")
	fid.write(".. tocTree::\n")
	fid.write("   :maxdepth: 1\n\n")
	for item in dBiz:
		fid.write("   %s\n" % os.path.split(item)[1].replace(".rst", ""))
	fid.write("\n\n")

	fid.write("Dabo - ui\n")
	fid.write("=========\n\n")
	fid.write(".. tocTree::\n")
	fid.write("   :maxdepth: 1\n\n")
	for item in dUi:
		fid.write("   %s\n" % os.path.split(item)[1].replace(".rst", ""))
	fid.write("\n\n")

	fid.write("Dabo - ui dialogs\n")
	fid.write("=================\n\n")
	fid.write(".. tocTree::\n")
	fid.write("   :maxdepth: 1\n\n")
	for item in dUid:
		fid.write("   %s\n" % os.path.split(item)[1].replace(".rst", ""))
	fid.write("\n\n")

	fid.write("Dabo - ui other\n")
	fid.write("=================\n\n")
	fid.write(".. tocTree::\n")
	fid.write("   :maxdepth: 1\n\n")
	for item in dUix:
		fid.write("   %s\n" % os.path.split(item)[1].replace(".rst", ""))
	fid.write("\n\n")

	fid.write("Dabo - ui datanav\n")
	fid.write("=================\n\n")
	fid.write(".. tocTree::\n")
	fid.write("   :maxdepth: 1\n\n")
	for item in dLibD:
		fid.write("   %s\n" % os.path.split(item)[1].replace(".rst", ""))
	fid.write("\n\n")

	fid.write("Dabo - lib\n")
	fid.write("==========\n\n")
	fid.write(".. tocTree::\n")
	fid.write("   :maxdepth: 1\n\n")
	for item in dLib:
		fid.write("   %s\n" % os.path.split(item)[1].replace(".rst", ""))
	for item in dLibA:
		fid.write("   %s\n" % os.path.split(item)[1].replace(".rst", ""))
	fid.write("\n\n")


	#
	# a hack to get rid of the toc warning for these
	fid.write(".. tocTree::\n")
	fid.write("   :glob:\n")
	fid.write("   :hidden:\n\n")

	fid.write("   dabo.biz_module\n")
	fid.write("   dabo.dabo_module\n")
	fid.write("   dabo.db_module\n")
	fid.write("   dabo.lib_module\n")
	fid.write("   dabo.ui_module\n")
	fid.write("   dabo.ui*\n")

	fid.close()
	
	WriteUiPackageIndex(dUi, dUix, dUid, dLibD)

def WriteUiPackageIndex(dUi, dUix, dUid, dLibD):

	fid = open("dabo.ui_module.rst", "wt")
	fid.write(imagesLinks + "\n")
	fid.write(".. _dabo.ui:\n\n")
	fid.write("=================================\n")
	fid.write("|doc_title| **dabo - ui package**\n")
	fid.write("=================================\n\n")

	fid.write("Widgets and sizers\n")
	fid.write("==================\n\n")
	fid.write(".. tocTree::\n")
	fid.write("   :maxdepth: 1\n\n")
	for item in dUi:
		fid.write("   %s\n" % os.path.split(item)[1].replace(".rst", ""))
	fid.write("\n\n")

	fid.write("Dialogs\n")
	fid.write("========\n\n")
	fid.write(".. tocTree::\n")
	fid.write("   :maxdepth: 1\n\n")
	for item in dUid:
		fid.write("   %s\n" % os.path.split(item)[1].replace(".rst", ""))
	fid.write("\n\n")

	fid.write("Dabo - ui other\n")
	fid.write("=================\n\n")
	fid.write(".. tocTree::\n")
	fid.write("   :maxdepth: 1\n\n")
	for item in dUix:
		fid.write("   %s\n" % os.path.split(item)[1].replace(".rst", ""))
	fid.write("\n\n")

	fid.write("Dabo - ui datanav\n")
	fid.write("=================\n\n")
	fid.write(".. tocTree::\n")
	fid.write("   :maxdepth: 1\n\n")
	for item in dLibD:
		fid.write("   %s\n" % os.path.split(item)[1].replace(".rst", ""))
	fid.write("\n\n")
	fid.close()

def WriteLayout(folder):

	if folder in [normalHtml, singleHtml]:
		layout = htmlLayout
	else:
		layout = otherLayout

	fid = open("source/_templates/layout.html", "wt")
	fid.write(layout)
	fid.close()


def WriteIndex(folder):

	if folder in [normalHtml, singleHtml]:
		fileName = "index_normal.rst"
	elif folder == helpHtml:
		fileName = "index_htmlhelp.rst"
	else:
		fileName = "index_latex.rst"

	fid = open("_rst_basefiles/"+fileName, "rt")
	text = fid.read()
	fid.close()

	fid = open("source/index.rst", "wt")
	fid.write(text)
	fid.close()

	raw = FindRawModules()
	return raw


def FindRawModules():

	fid = open("_rst_basefiles/tree_module_list.rst", "rt")
	found = False
	moduleList = ""
	for tline in fid:

		tline = tline.strip()
		mod, name = tline.split(',')

		moduleList += rawhtmlsingle % (mod+".html", name) + "\n"

	fid.close()

	return rawhtmlfull % moduleList

def MakeRst(builder):
	WriteLayout(builder)
	raw = WriteIndex(builder)

	if builder == normalHtml:

		# create the *_module.rst for top layer and packages
		MakeInitDocs(topLayer, raw)
		# create the module docs for the top level
		MakeModuleDocs(None, raw)
		# now process all packages defined in subPackages
		for pkg in subPackages:
			MakeModuleDocs(pkg, raw)
			# now the ones for packages in packages
			if subSubPackages.has_key(pkg):
				for sPkg in subSubPackages[pkg]:
					MakeModuleDocs(pkg + '.' + sPkg, raw)

		WriteGeneralIndex()


def FractSec(s):

	min, s = divmod(s, 60)
	h, min = divmod(min, 60)
	return h, min, s


start = time.time()

args = sys.argv[1:]

if not args:
	clearOldRst = False
else:
	# we just assume that is what was wanted
	clearOldRst = True
		
print "================================================"
print "removing files from previous run in %s" % rstTempFolder
print "================================================"
remRst = glob.glob(rstTempFolder + "\*.rst")
for item in remRst:
	os.remove(item)


if clearOldRst:
	print "================================================"
	print "removing files, forcing a full rebuild %s" % docFolder
	print "================================================"

	oldRst = glob.glob(docFolder + "\*.rst")
	for item in oldRst:
		os.remove(item)

# generate .rst in tempFolder
MakeRst(normalHtml)

# write picture index to a file
genNote = """This file is generated by makeRST.py and used by genGallery.py,
please do not change it by hand.
"""
indexF = open(os.path.join(baseFolder, "galleryToClassIndex.py"), "w")
indexF.write("# -*- coding: utf-8 -*-#\n\n")
indexF.write('"""%s"""\n\n' % genNote)
indexF.write("pictureIndex = {}\n")
for item in pictureIndex:
	indexF.write("pictureIndex['%s'] = '%s'\n" % (item, pictureIndex[item]))
indexF.close()

# compare files in rstTempFolder to docFolder, if changed copy to docFolder
print "========================================"
print "check if file(s) have changed"
print "========================================"

checkRst = glob.glob(rstTempFolder + "\*.rst")
for item in checkRst:
	path, fileName = os.path.split(item)
	tmpFile = os.path.join(rstTempFolder, fileName)
	docFile = os.path.join(docFolder, fileName)
	if os.path.isfile(docFile):
		if not filecmp.cmp(tmpFile, docFile, False):
			# file has changed, copy it
			shutil.copy(tmpFile, docFile)
			print "changed file, copy to: %s" % docFile
	else:
		shutil.copy(tmpFile, docFile)
		print "new file, copy to: %s" % docFile		


current = time.time()
h, m, s = FractSec(int(current - start))

print "\nDabo .rst files created. Elapsed time %02d:%02d:%02d"%(h, m, s)

