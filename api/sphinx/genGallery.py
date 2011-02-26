# -*- coding: utf-8 -*-#

import os
import pydoc
import glob, re, sys, warnings

import galleryToClassIndex

# generate a thumbnail gallery of examples
template = """\
{%% extends "layout.html" %%}
{%% set title = "Thumbnail gallery" %%}


{%% block body %%}

<h3>Click on any image to see full size image, or click on the caption to go to the relevant documentation</h3>
<br/>

%s
{%% endblock %%}
"""

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
			if m in method:
				if "." not in m:
					index = name.rfind(".")
					newname = name[0:index] + "." + m
					index2 = newname.rfind(".")
					othername = newname[0:index2] + "." + m
					
					if newname == method:
						line = line.replace(newM, ":meth:`~%s`"%method)
						newMatches.remove(m)
						break
					elif othername.endswith(method):
						line = line.replace(newM, ":meth:`~%s`"%method)
						newMatches.remove(m)
						break
					elif m == "CmpThumb":
						line = line.replace(newM, ":meth:`~thumbnailctrl.CmpThumb`")
						newMatches.remove(m)
						break
						
				else:
					if method.endswith(m):
						line = line.replace(newM, ":meth:`%s() <%s>`"%(m, method))
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


def gen_gallery(app, doctree):

##    print 'gen_gallery: %s, %s' % (app, app.builder.name)
	
	if app.builder.name not in ['html', 'singlehtml']:
		return

	outdir = app.builder.outdir
##    print outdir
##    print app.builder.srcdir
##    rootdir = '_staticGallery/'

	link = '<div class="gallery_class">'
##	<table><caption align="bottom"><b>%s</b></caption>
	link_template = """\
	<table><caption align="bottom"><a href="%s"<b>%s</b></a</caption>
	<tr><td><a href="%s"><img src="%s" border="5" alt="%s" width="100" height="100"/></a></td></tr>
	</table>"""
	
	data = []
	thumbnails = {}
	rows = ["<br/>", link]

	# need to join srcdir
	for item in sorted(glob.glob(os.path.join(app.builder.srcdir, "_static/*_thumb.png"))):
##        print "item: %s" % item
		path, filename = os.path.split(item)
		basename, ext = os.path.splitext(item)
		
		# need to get rid of srcdir as links have to be relative
		basename = basename.replace(app.builder.srcdir + "\\", "")
		item = item.replace(app.builder.srcdir + "\\", "")

		realfile = basename[0:-6] + ext

		realfile = realfile.replace("\\", "/")
		item = item.replace("\\", "/")
		# Create thumbnails based on images in tmpdir, and place
		# them within the build tree
		linkName = ""
		linkKey = basename[8:-6]
		linkKeyL = len(linkKey)
		if linkKey[linkKeyL-1:linkKeyL].isdigit():
			linkKey = linkKey[:linkKeyL-1]
   		if galleryToClassIndex.pictureIndex.has_key(linkKey):
			# lets find the documentation link for this image
			linkName = galleryToClassIndex.pictureIndex[linkKey]
		else:
			linkName = "gallery.html"
##		print "base: %s" % basename
##		print "base2: %s" % basename[8:-6]
##		print "linkKey: %s" % linkKey
##		print realfile
##		print item
##		print linkName
##		print link_template

		rows.append(link_template % (linkName, basename[8:-6], realfile, item, basename[8:-6]))

	rows.append("</div>")
	rows.append('<br clear="all"> ')
	
##    # Only write out the file if the contents have actually changed.
##    # Otherwise, this triggers a full rebuild of the docs
	content = template % '\n'.join(rows)
##    print content
	gallery_path = os.path.join(app.builder.srcdir, '_templates', 'gallery.html')
##    print gallery_path

	fh = file(gallery_path, 'w')
	fh.write(content)
	fh.flush()
	fh.close()

	
def setup(app):

	app.connect('env-updated', gen_gallery)


