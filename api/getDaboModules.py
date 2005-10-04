import dabo
import dabo.common
dabo.ui.loadUI("wx")


def getDaboModules():
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

	return modules

def getDaboClasses():
	classes = []
	for module in (dabo, dabo.db, dabo.biz, dabo.ui):
		for i in dir(module):
			c = module.__dict__[i]
			if type(c) == type and issubclass(c, dabo.common.dObject):
				classes.append(c)
	def sortfunc(a,b):
		return cmp(a.__name__, b.__name__)
		
	classes.sort(sortfunc)
	return classes
