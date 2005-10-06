#!/usr/bin/env python

import datetime
import inspect
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
## book).  --pkm

d = datetime.datetime.now()

footerString = """
<hr>
Dabo %s (rev. %s)<br>
%s""" % (dabo.version["version"],
         dabo.version["revision"],
         d.strftime("%e %b %Y %T"))


def formatDoc(doc):
	"""Strip indentation whitespace from the docstring."""
	docLines = doc.splitlines()
	if len(docLines) == 0:
		return doc

	# All whitespace from first line:
	docLines[0] = docLines[0].strip()

	# Use the indentation from the second line (third if the second is blank)
	# for the rest of the lines:
	indent = ""
	if len(docLines) > 1:
		if len(docLines[1].strip()) > 0:
			# use indent from this line
			for l in docLines[1]:
				if l.isspace():
					indent += l
				else:
					break
			docLines[1] = docLines[1].strip()
		else:
			if len(docLines) > 2:
				if len(docLines[2].strip()) > 0:
					# use indent from this line
					for l in docLines[2]:
						if l.isspace():
							indent += l
						else:
							break
					docLines[2] = docLines[2].strip()
	for idx, line in enumerate(docLines):
		if line.find(indent) == 0:
			line = line.replace(indent, "", 1)
			docLines[idx] = line

	doc = '\n'.join(docLines)
	doc = doc.replace("<", "&lt;")
	return doc
	
classes = getDaboClasses()

def getApiDoc(cls, outputType="html-single"):
	PEM_COLUMNS = float(3)  ## float simply for round() to work right

	className = cls.__name__
	classDoc = cls.__doc__
	if classDoc is None:
		classDoc = ""
	classDoc = formatDoc(classDoc)

	html = """
<h1>Class %(className)s</h1>
<pre>%(classDoc)s</pre>
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
<table border="1" cellpadding="20" cellspacing="0">
"""
	for prop in propList:
		d = cls.getPropertyInfo(prop)
		if d["doc"] is None:
			d["doc"] = ""
		d["doc"] = formatDoc(d["doc"])	

		d["definedInString"] = ""
		if d["definedIn"] != cls:
			filename = "./%s.%s.html" % (d["definedIn"].__module__, d["definedIn"].__name__)
			if d["definedIn"] in classes:
				link = """<a href="%s">%s</a>""" % (filename, d["definedIn"].__name__)
			else:
				link = "%s" % d["definedIn"].__name__
			d["definedInString"] = """<br><i>(inherited from <b>%s</b>)</i>""" % link

		html += """
	<tr>
		<td valign="top">
			<b><a name="Properties_%(name)s">%(name)s</a></b>
			<pre>%(doc)s</pre>
			%(definedInString)s
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
<table border="1" cellpadding="20" cellspacing="0">
"""
	for event in eventList:
		e = dEvents.__dict__[event]
		d = {"name": event,
		     "doc": e.__doc__}
		if d["doc"] is None:
			d["doc"] = ""
		d["doc"] = formatDoc(d["doc"])	

		html += """
	<tr>
		<td valign="top">
			<b><a name="Events_%(name)s">%(name)s</a></b><br>
			<pre>%(doc)s</pre>
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
<table border="1" cellpadding="20" cellspacing="0">
"""
	for method in methodList:
		m = None
		definedIn = None
		for o in cls.__mro__:
			try:
				m = o.__dict__[method]
				definedIn = o
			except KeyError:
				continue
			break
		if m is None:
			continue

		args = inspect.getargspec(m)
		args = inspect.formatargspec(args[0], args[1], args[2], args[3])

		d = {"name": method,
		     "doc": m.__doc__,
		     "args": args}
		if d["doc"] is None:
			d["doc"] = ""
		d["doc"] = formatDoc(d["doc"])	

		d["definedInString"] = ""
		if definedIn != cls:
			filename = "./%s.%s.html" % (definedIn.__module__, definedIn.__name__)
			if definedIn in classes:
				link = """<a href="%s">%s</a>""" % (filename, definedIn.__name__)
			else:
				link = "%s" % definedIn.__name__
			d["definedInString"] = """<br><i>(inherited from <b>%s</b>)</i>""" % link


		html += """
	<tr>
		<td valign="top">
			<b><a name="Methods_%(name)s">%(name)s%(args)s</a></b>
			<pre>%(doc)s</pre>
			%(definedInString)s
		</td>
	</tr>
""" % d
	html += """
</table>
"""
	html += footerString
	return html

if os.path.exists("./daboApiDoc"):
	for f in os.listdir("./daboApiDoc"):
		os.remove(os.path.join("./daboApiDoc", f))
	os.rmdir("./daboApiDoc")	
	#sys.exit("Please move existing ./daboApiDoc out of the way first.")

os.mkdir("./daboApiDoc")
os.chdir("./daboApiDoc")


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

remove = []
for idx, class_ in enumerate(classes):
	if ("dabo.d" in class_.__module__ or "dabo.common" in class_.__module__) \
	and "dabo.db" not in class_.__module__:
		html += """
			<a href="./%s.%s.html">%s</a><br>""" % (class_.__module__, class_.__name__,
		                                          class_.__name__)
		remove.insert(0,idx)
for i in remove:
	del(classes[i])

html += """
			<br>
			<br>
		</td>
		<td width="33%">&nbsp;</td>
	</tr>
	<tr>
		<td width="33%" valign="top">
			<b>db:</b><br>"""

remove = []
for idx, class_ in enumerate(classes):
	if "dabo.db" in class_.__module__:
		html += """
			<a href="./%s.%s.html">%s</a><br>""" % (class_.__module__, class_.__name__,
		                                     class_.__name__)
		remove.insert(0, idx)

for i in remove:
	del(classes[i])

html += """
		</td>
		<td width="33%" valign="top">
			<b>biz:</b><br>"""

remove = []
for idx, class_ in enumerate(classes):
	if "dabo.biz" in class_.__module__:
		html += """
			<a href="./%s.%s.html">%s</a><br>""" % (class_.__module__, class_.__name__,
		                                     class_.__name__)
		remove.insert(0, idx)
for i in remove:
	del(classes[i])

html += """
		</td>
		<td width="33%" valign="top">
			<b>ui:</b><br>"""

remove = []
for idx, class_ in enumerate(classes):
	if "dabo.ui":
		html += """
			<a href="./%s.%s.html">%s</a><br>""" % (class_.__module__, class_.__name__,
		                                     class_.__name__)
		remove.insert(0, idx)
for i in remove:
	del(classes[i])

html += """
		</td>
	</tr>
</table>
"""

html += footerString

filename = "index.html"
f = open(filename, "w")
f.write(html)
f.close()
