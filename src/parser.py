from grammar import *

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


integer.addParseAction(lambda s,l,tok: int(tok[0]))

def parseDirection(s,l,tok):
	match = tok[0]
	if match == "=>":
		return "C2S"
	elif match == "<=":
		return "S2C"
	else:
		return "BOTH"
direction.addParseAction(parseDirection)

def parseParameter(s,l,tok):
	match = tok[0]
	return Parameter(match[0], match[1])
parameter.addParseAction(parseParameter)

def parseModuleParameter(s,l,tok):
	match = tok[0]
	return ModuleParameter(match[1], match[2])
moduleparam.addParseAction(parseModuleParameter)

def parseMessage(s,l,tok):
	match = tok[0]
	return Message(match[0], match[1], match[2], match[3].asList())
message.addParseAction(parseMessage)

def parseDeclarations(s,l,tok):
#	print
	return "\r\ntoklen=%d\r\n%s\r\n" % ( len(tok), "".join([str(t) for t in tok]) )
	#return "toklen=%d\r\n%s\r\n%s" % ( len(tok), tok[0], tok[1] )
	
#declarations.addParseAction(parseDeclarations)

def parseModule(s,l,tok):
	match = tok[0]
	name = match[0]
	params = []
	messages = []
	modules = []
	
	for decl in match[1:]:
		if isinstance(decl, ModuleParameter):
			params.append(decl)
		elif isinstance(decl, Message):
			messages.append(decl)
		elif isinstance(decl, Module):
			modules.append(decl)
			
	return Module(name, params, messages, modules)


module.addParseAction(parseModule)

if __name__ == "__main__":
	import sys, os, os.path
	if len( sys.argv ) == 0:
		sys.exit(-1)
		
	filename = sys.argv[1]
	if not os.path.exists( filename ):
		sys.exit(-1)
		
	f = open(filename)
	input = "".join( f.readlines() )
	
	print npsl.parseString( input )
	
