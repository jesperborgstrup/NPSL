import struct

class MessageHandler:
	
	client = None
	
	def __init__(self, client):
		self.client = client
		
	def handle(self, message):
		pass
	
	def parse(self, message, length):
		return message[:length], message[length:]
		
	def parse_struct(self, message, format):
		if format == "":
			return None, message
		else:
			try:
				str, message = self.parse( message, struct.calcsize( format ) )
				return ( struct.unpack( format, str )[0], message )
			except:
				raise RuntimeError("PARSE")
	
	def log(self, str, level=5):
		return self.client.log( "Handler> %s" % (str), level)
