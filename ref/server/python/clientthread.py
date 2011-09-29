import threading
import struct
import socket
from settings import Settings
from mainmessagehandler import MainMessageHandler


class ClientThread( threading.Thread ):
	server = None
	client = None
	host = None
	port = None
	handler = None
	
	def __init__(self, server, clientAddr):
		threading.Thread.__init__(self)
		self.server = server
		self.client, address = clientAddr
		self.host, self.port = address
		self.handler = MainMessageHandler( self )

		self.server.interface.client_connected(self.host, self.port)
		self.log( "Connected", level=4 )
		
		self.prefix_length = struct.calcsize( Settings.PREFIX_LENGTH_FORMAT )
		
	def run(self):
		while 1:
			try:
				messageLengthBinary = self.recv( self.prefix_length )
				messageLength = struct.unpack( Settings.PREFIX_LENGTH_FORMAT, messageLengthBinary )[0]
				print "Length=%d" % messageLength
				
				message = self.recv( messageLength )
				self.handle_message( message )
			except RuntimeError as e:
				if not self.exception( e ):
					break
		
		self.close()
	
	"""
	Receive length bytes from the socket.
	"""
	def recv(self, length):
		self.log( "recv(%d)" % length, level=11)
		msg = ''
		while len(msg) < length:	
			chunk = self.client.recv(length-len(msg))
			if chunk == '':
				raise RuntimeError("BROKEN")
			msg = msg + chunk
		self.log( "recv(%d) finished" % length, level=11)
		return msg
	
	def handle_message(self, message):
		self.handler.handle( message )

	def log(self, str, level=5):
		return self.server.log( "%s:%s> %s" % (self.host, self.port, str), level)
	
	"""
	Shutdown the socket connection.
	"""
	def close(self):
		self.client.shutdown( socket.SHUT_RDWR )
		self.client.close()
		self.server.interface.client_disconnected(self.host, self.port)
		self.log( "Disconnected", level=4 )
		
	"""
	Reports that an exception occured in the socket.
	Returns a boolean value indicating whether or not operation of the socket
	should continue.
	"""
	def exception(self, e):
		msg = str(e)
		if msg == "BROKEN":
			return self.connection_broken()
		if msg == "PARSE":
			return self.parse_error()
			

	"""
	Called when the connection is broken.
	"""
	def connection_broken(self):
		self.log( "Socket connection broken" )
		return False
	
	"""
	Called upon a parse error
	"""
	def parse_error(self):
		self.log( "Parse error" )
		return False