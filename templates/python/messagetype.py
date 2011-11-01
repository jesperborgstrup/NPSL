{% set output_dest, package = "messagetype.py", "common" %}
class MessageType:
	id = None
	name = None
	params = []
	messages = {}
	
	def __init__(self, id, name, params=[], messages={}):
		self.id = id
		self.name = name
		self.params = params
		self.messages = messages

	def __str__(self):
		return "MessageType(%d, %s): params%s, messages%s" % (self.id, self.name, self.params, self.messages)