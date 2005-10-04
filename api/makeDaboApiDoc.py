#!/usr/bin/env python

import os
import sys
import dabo
dabo.ui.loadUI("wx")
import dabo.dEvents as dEvents
from getDaboModules import getDaboClasses

## This is my new attempt at API documentation, which doesn't use epydoc and 
## will do a better job of only grabbing the things we actually want to
## to document. It is pretty basic now (4 Oct 2005), but does print out the
## PEM's for every Dabo object it finds, although it will need some help
## finding some things (dSecurityManager, dReportWriter, ...). I want to
## add cascading stylesheets and the ability to print to PDF (for an API
## book). Next step: make the item listings for each PEM jump to the docstring
## for those items. For methods, include the method signature. The detailed
## docstrings will be at the bottom of each page.  --pkm


def getApiDoc(cls, outputType="html-single"):
	PEM_COLUMNS = float(3)  ## float simply for round() to work right

	className = cls.__name__
	classDoc = cls.__doc__
	if classDoc is None:
		classDoc = ""
	classDoc = "<br>".join(classDoc.split("\n"))

	html = """
<h1>Class %(className)s</h1>
<p>%(classDoc)s</p>
<hr>
""" % locals()

	def getListing(name, items):
		html = """
<h2>%(name)s</h2>
<table width="100%%" cellpadding="5" cellspacing="0" border="0">
""" % locals()

		for idx, item in enumerate(items):
			definedHere = (cls.__dict__.has_key(item))
			if idx % PEM_COLUMNS == 0:
				if idx > 0:
					html += """	</tr>
"""
				html += """	<tr>
"""
			if definedHere:
				html += """		<td><b><a href="#%(name)s_%(item)s">%(item)s</a></b></td>
""" % locals()
			else:
					html += """		<td><a href="#%(name)s_%(item)s">%(item)s</a></td>
""" % locals()

		html += """
	</tr>
</table>
<hr>
"""
		return html


		
	# Property, Event, Method Listings:
	propList = cls.getPropertyList(refresh=True)
	eventList = cls.getEventList()
	methodList = cls.getMethodList(refresh=True)

	html += getListing("Properties", propList)
	html += getListing("Events", eventList)
	html += getListing("Methods", methodList)

	# Expanded entries - properties:
	html += """
<br><br><br>
<h2>Properties</h2>
<table border="0" width="100%" cellpadding="20" cellspacing="0">
"""
	for prop in propList:
		d = cls.getPropertyInfo(prop)
		if d["doc"] is None:
			d["doc"] = ""
		d["doc"] = "<br>".join(d["doc"].split("\n"))

		html += """
	<tr>
		<td valign="top">
			<b><a name="Properties_%(name)s">%(name)s</a></b><br>
			%(doc)s
		</td>
	</tr>
""" % d
	html += """
</table>
"""

	# Expanded entries - events:
	html += """
<br><br><br>
<h2>Events</h2>
<table border="0" width="100%" cellpadding="20" cellspacing="0">
"""
	for event in eventList:
		e = dEvents.__dict__[event]
		d = {"name": event,
		     "doc": e.__doc__}
		if d["doc"] is None:
			d["doc"] = ""
		d["doc"] = "<br>".join(d["doc"].split("\n"))

		html += """
	<tr>
		<td valign="top">
			<b><a name="Events_%(name)s">%(name)s</a></b><br>
			%(doc)s
		</td>
	</tr>
""" % d
	html += """
</table>
"""

	# Expanded entries - methods:
	html += """
<br><br><br>
<h2>Methods</h2>
<table border="0" width="100%" cellpadding="20" cellspacing="0">
"""
	for method in methodList:
		m = None
		for o in cls.__mro__:
			try:
				m = o.__dict__[method]
			except KeyError:
				continue
			break
		if m is None:
			continue
		d = {"name": method,
		     "doc": m.__doc__}
		if d["doc"] is None:
			d["doc"] = ""
		d["doc"] = "<br>".join(d["doc"].split("\n"))

		html += """
	<tr>
		<td valign="top">
			<b><a name="Methods_%(name)s">%(name)s()</a></b><br>
			%(doc)s
		</td>
	</tr>
""" % d
	html += """
</table>
"""

	return html

if os.path.exists("./daboApiDoc"):
	for f in os.listdir("./daboApiDoc"):
		os.remove(os.path.join("./daboApiDoc", f))
	os.rmdir("./daboApiDoc")	
	#sys.exit("Please move existing ./daboApiDoc out of the way first.")

os.mkdir("./daboApiDoc")
os.chdir("./daboApiDoc")


classes = getDaboClasses()
for class_ in classes:
	filename = "%s.%s.html" % (class_.__module__, class_.__name__)
	html = getApiDoc(class_)
	f = open(filename, "w")
	f.write(html)
	f.close()


html = """
<table border="0" cellpadding="5" cellspacing="0" width="100%">
	<tr>
		<td width="33%">&nbsp;</td>
		<td width="33%" valign="top">
			<b>Dabo:</b><br>"""

for class_ in classes:
	if "dabo.d" in class_.__module__ and "dabo.db" not in class_.__module__:
		html += """
			<a href="./%s.%s.html">%s</a><br>""" % (class_.__module__, class_.__name__,
		                                     class_.__name__)

html += """
		</td>
		<td width="33%">&nbsp;</td>
	</tr>
	<tr>
		<td width="33%" valign="top">
			<b>db:</b><br>"""

for class_ in classes:
	if "dabo.db" in class_.__module__:
		html += """
			<a href="./%s.%s.html">%s</a><br>""" % (class_.__module__, class_.__name__,
		                                     class_.__name__)

html += """
		</td>
		<td width="33%" valign="top">
			<b>biz:</b><br>"""

for class_ in classes:
	if "dabo.biz" in class_.__module__:
		html += """
			<a href="./%s.%s.html">%s</a><br>""" % (class_.__module__, class_.__name__,
		                                     class_.__name__)

html += """
		</td>
		<td width="33%" valign="top">
			<b>ui:</b><br>"""

for class_ in classes:
	if "dabo.ui" in class_.__module__:
		html += """
			<a href="./%s.%s.html">%s</a><br>""" % (class_.__module__, class_.__name__,
		                                     class_.__name__)

html += """
		</td>
	</tr>
</table>
"""

filename = "index.html"
f = open(filename, "w")
f.write(html)
f.close()
