class Module:
	name = None
	id = None
	messagehandler = None
	
	def __init__(self, name, id, messagehandler):
		self.name = name
		self.id = id
		self.messagehandler = messagehandler