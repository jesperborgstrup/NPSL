class Message:
	name = None
	params = {}
	parent = None
	child = None
	
	def __init__(self, name, params={}, child=None):
		self.name = name
		self.params = params
		self.child = child
		if child != None:
			child.parent = self
			
	def __str__(self):
		childstr = ""
		if self.child != None:
			childstr = ", child(%s)" % str( self.child )
		return "Message(%s): params%s%s" % (self.name, self.params, childstr)