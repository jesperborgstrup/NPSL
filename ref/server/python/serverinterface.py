class ServerInterface:
	
	def __init__(self):
		pass
	
	def client_connected(self, host, port):
		print "Client connected:", host, port
		
	def client_disconnected(self, host, port):
		print "Client disconnected:", host, port
		
	def message(self, message):
		print "Message: %s" % message
