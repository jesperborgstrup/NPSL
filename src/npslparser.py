from grammar import integer, boolean, direction, parameter, moduleparam, message, module, setting, settings, npsl

integer.addParseAction(lambda s,l,tok: int(tok[0]))
boolean.addParseAction(lambda s,l,tok: True if tok[0]=="true" else False)

def splitDirections(item):
	if item["direction"] == "both":
		c = item.copy()
		s = item.copy()
		c["direction"] = "c2s"
		s["direction"] = "s2c"
		return [c,s]
	return [item]

def parseDirection(s,l,tok):
	match = tok[0]
	if match == "=>":
		return "c2s"
	elif match == "<=":
		return "s2c"
	else:
		return "both"
direction.addParseAction(parseDirection)

def parseParameter(s,l,tok):
	match = tok[0]
	return {"type": "parameter", "name": match[0], "type": match[1]}
parameter.addParseAction(parseParameter)

def parseModuleParameter(s,l,tok):
	match = tok[0]
	return {"type": "moduleparameter", "direction": match[1], "parameter": match[2]}
moduleparam.addParseAction(parseModuleParameter)

def parseMessage(s,l,tok):
	match = tok[0]
	return {"type": "message", "direction": match[0], "id": match[1], "name": match[2], "parameters": match[3].asList()}
message.addParseAction(parseMessage)

def makeModule(name,Id,items):
	params = []
	messages = []
	modules = []
	settings = {}
	
	for decl in items:
		if decl["type"] == "moduleparameter":
			params.extend( splitDirections( decl ) )
		elif decl["type"] == "message":
			messages.extend( splitDirections( decl ) )
		elif decl["type"] == "module":
			modules.append(decl)
		elif decl["type"] == "settings":
			settings.update(decl["settings"])
			
	return {"name": name, "id": Id, "parameters": params, "messages": messages, "modules": modules, "type": "module", "settings": settings}

def parseModule(s,l,tok):
	match = tok[0]
	name = match[0]
	Id = match[1]
	return makeModule(name, Id, match[2:])

module.addParseAction(parseModule)

def parseSetting(s,l,tok):
	match = tok[0]
	return {"type": "setting", "name": match[0], "value": match[1]}
	
setting.addParseAction(parseSetting)

def makeSettings(settings):
	dict = {}
	for setting in settings:
		dict[setting["name"]] = setting["value"] 
	return {"type": "settings", "settings": dict}

def parseSettings(s,l,tok):
	match = tok[0]
	return makeSettings( match[1] )
	
settings.addParseAction(parseSettings)

def parseNPSL(s,l,tok):
	return makeModule("main", -1, tok)

npsl.addParseAction(parseNPSL)
	
