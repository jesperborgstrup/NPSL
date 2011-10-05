class Parameter:
	def __init__(self, name, type):
		self.name = name
		self.type = type
	def __repr__(self):
		return "%s, %s" % (self.name,self.type)

class Message:
	def __init__(self, dir, id, name, params):
		self.dir = dir
		self.id = id
		self.name = name
		self.params = params
	def __repr__(self):
		return "Message(%s, %d)" % (self.name, len(self.params))
		
class ModuleParameter:
	def __init__(self, dir, param):
		self.dir = dir
		self.param = param
	def __repr__(self):
		return "ModuleParameter(%s)" % self.param
	
class Module:
	def __init__(self, name, params, messages, modules):
		self.name = name
		self.params = params
		self.messages = messages
		self.modules = modules
	def __repr__(self):
		return "Module(%s, %s, %s, %s)" % (self.name, repr(self.params), repr(self.messages), repr(self.modules))

