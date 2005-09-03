#!/usr/bin/env python

# Run this script to generate the epydoc documentation.

import sys
import types
import os
import dabo
dabo.ui.loadUI("wx")

_outputType = "html"
#_outputType = "pdf"

# I think "included" is the nicest format:
_inheritanceFormat = "included"   ## lists all attributes together, with text that shows where inherited from
#_inheritanceFormat = "grouped"   ## default epydoc: groups the attributes under the classes that define them
#_inheritanceFormat = "listed"    ## lists the attributes next to the class that defines them

_version = dabo.__version__.version

_name = "Dabo %s (Revision %s)" % (_version["version"], _version["revision"])
_url = "http://dabodev.com"

modules = [
	"dabo", 
	"dabo.dApp", 
	"dabo.dSecurityManager", 
	"dabo.dUserSettingProvider", 
	"dabo.db", 
	"dabo.db.dConnection",
	"dabo.db.dCursorMixin", 
	"dabo.db.dConnectInfo", 
	"dabo.db.dbMySQL",
	"dabo.db.dbPostgreSQL", 
	"dabo.db.dbFirebird",
	"dabo.db.dbSQLite",
	"dabo.biz", 
	"dabo.biz.dBizobj",
	"dabo.ui",
	"dabo.ui.uiwx",]

# Now we dynamically gather the ui classes to document:
controlClasses = []
formClasses = []
sizerClasses = []

for i in dir(dabo.ui):
	item = dabo.ui.__dict__[i]
	if type(item) == type:
		if "Mixin" not in item.__name__:
			if issubclass(item, dabo.ui.dControlMixin):
				controlClasses.append(item)
			if issubclass(item, dabo.ui.dFormMixin):
				formClasses.append(item)
			if issubclass(item, dabo.ui.dSizerMixin):
				sizerClasses.append(item)

print "Control Classes:"
for i in controlClasses:
	modules.append("dabo.ui.uiwx.%s" % i.__name__)
	print "\t %s" % i.__name__

print "Form Classes:"
for i in formClasses:
	modules.append("dabo.ui.uiwx.%s" % i.__name__)
	print "\t %s" % i.__name__

print "Sizer Classes:"
for i in sizerClasses:
	modules.append("dabo.ui.uiwx.%s" % i.__name__)
	print "\t %s" % i.__name__


modulestring = " ".join(modules)
os.system("""python ./epydoc_cli.py --%s --inheritance %s --url "%s" --name "%s" --no-private %s""" % (_outputType, 
		_inheritanceFormat, _url, _name, modulestring))
