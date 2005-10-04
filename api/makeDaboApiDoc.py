#!/usr/bin/env python

import os
import sys
import dabo
dabo.ui.loadUI("wx")
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
				html += """		<td><b><a href="#prop_%(item)s">%(item)s</a></b></td>
""" % locals()
			else:
					html += """		<td><a href="#prop_%(item)s">%(item)s</a></td>
""" % locals()

		html += """
	</tr>
</table>
<hr>
"""
		return html
		
	# Property, Event, Method Listings:
	html += getListing("Properties", cls.getPropertyList(refresh=True))
	html += getListing("Events", cls.getEventList())
	html += getListing("Methods", cls.getMethodList(refresh=True))

	return html

if os.path.exists("./daboApiDoc"):
	sys.exit("Please move existing ./daboApiDoc out of the way first.")

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
