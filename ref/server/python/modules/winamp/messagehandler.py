from ..messagehandler import MessageHandler
from types import types

class WinampMessageHandler(MessageHandler):
	
	def __init__(self, client):
		MessageHandler.__init__(self, client)
		
	def handle(self, message):
		msg, message = self.parse_struct( message, ">I" )
		
		if types.has_key( msg ):
			self.log( types[msg][0] )
		else:
			self.log( "No message %d" % msg )

	def log(self, str):
		print "Winamp Handler: %s" % str