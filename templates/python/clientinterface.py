{% set output_dest, package = "clientinterface.py", "client" %}

class ClientInterface:
	
	def __init__(self):
		pass
	
	def connected(self, otherend):
		print "%s:%s connected" % ( otherend.host, otherend.port )
		
	def disconnected(self, otherend):
		print "%s:%s disconnected" % ( otherend.host, otherend.port )
		
	def message(self, message, otherend):
		print "%s:%s> %s" % ( otherend.host, otherend.port, message )
