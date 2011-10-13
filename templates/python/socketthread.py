{% set output_dest, package = "socketthread.py", "common" %}

import threading
import struct
import socket
import traceback
import sys
from settings import Settings
from messagehandler import MessageHandler
from messagefactory import MessageFactory
import messages


class SocketThread( threading.Thread ):
	socket = None
	host = None
	port = None
	interface = None
	logger = None
	handler = None
	recvmessage = None
	sendmessage = None
	send = None
	
	def __init__(self, socketAddr, interface, logger, recvmessage, sendmessage):
		threading.Thread.__init__(self)
		self.socket, address = socketAddr
		self.host, self.port = address
		self.interface = interface

		if logger is None:
			self.logger = DummyLogger()
		else:
			self.logger = logger

		self.recvmessage = recvmessage
		self.handler = MessageHandler(self)
		self.sendmessage = sendmessage
		self.send = MessageFactory(mainmessage=sendmessage, socket=self.socket)

		self.interface.connected( self )

		self.prefix_length = struct.calcsize( Settings.PREFIX_LENGTH_FORMAT )
		
	def run(self):
		while 1:
			try:
				messageLengthBinary = self.recv( self.prefix_length )
				messageLength = struct.unpack( Settings.PREFIX_LENGTH_FORMAT, messageLengthBinary )[0]
				
				message = self.recv( messageLength )
				self.handle_message( message )
			except socket.error, (value, message):
				if not self.socket_error(value, message):
					break
			except RuntimeError as e:
				if not self.exception( e ):
					break
		
		self.close()
		
	def handle_message(self, message):
		self.interface.message( self.handler.handle( message, self.recvmessage )[0], self )
		
	def log(self, str, level=5):
		return self.logger.log( "%s:%s> %s" % (self.host, self.port, str), level)
	
	"""
	Receive length bytes from the socket.
	"""
	def recv(self, length):
		self.log( "recv(%d)" % length, level=11)
		msg = ''
		while len(msg) < length:	
			chunk = self.socket.recv(length-len(msg))
			if chunk == '':
				raise RuntimeError("BROKEN")
			msg = msg + chunk
		self.log( "recv(%d) finished" % length, level=11)
		return msg
	
	def socket_error(self, value, message):
		self.log( "ERROR %d (%s)" % (value, message) , level=1 )
		
		if value == 10054:
			return self.connection_broken()

		return False
		
	def close(self):
		self.socket.close()
		self.interface.disconnected( self )
		
	"""
	Shutdown the socket connection.
	"""
	def shutdown(self):
		self.socket.shutdown( socket.SHUT_RDWR )
		
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
		self.log( "Socket connection broken", level=7 )
		return False
	
	"""
	Called upon a parse error
	"""
	def parse_error(self):
		self.log( "Parse error" )
		return False
	
class DummyLogger:
	def log(self, str, level=5):
		pass
