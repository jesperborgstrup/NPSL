{% set output_dest, package = "server.py", "server" %}

import socket
import threading
import struct
import locale
import sys
import traceback
from settings import Settings
from clientthread import ClientThread

class Server(threading.Thread):
	threads = []
	backlog = 5
	host = None
	port = None
	interface = None
	logger = None
	
	def __init__(self, host='', port=1234, interface=None, logger=None):
		threading.Thread.__init__(self)
		self.port = port
		self.host = host
		self.interface = interface
		self.default_encoding = locale.getdefaultlocale()[1]

		if logger is None:
			self.logger = DummyLogger()
		else:
			self.logger = logger
		
	def run(self):
		try:
			self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.socket.bind((self.host,self.port))
			self.socket.listen(self.backlog)
			self.log( "Server started on %s:%d" % (self.host, self.port), 2 )
		except socket.error, (value, message):
			self.socket_error(value, message)
			return
		
		while 1:
			try:
				thread = ClientThread( self.socket.accept(), self, logger=self.logger )
				self.threads.append( thread )
				thread.start()
			except socket.error, (value, message):
				self.socket_error(value, message)
			except:
				self.log_exception()
				
	def log(self, str, level=5):
		self.logger.log(str, level)
		
	def log_exception(self):
		exc_type, exc_value, exc_traceback = sys.exc_info()
		lines = traceback.format_exception( exc_type, exc_value, exc_traceback )
		self.log("=== AN EXCEPTION OCCURED ===", level=1)
		[self.log(line.decode( self.default_encoding ), level=1) for line in lines]

	def socket_error(self, value, message):
		self.log( "ERROR %d (%s)" % (value, message.decode( self.default_encoding )) , level=1 )
		
	def stop(self):
		# Close all client sockets
		self.socket.shutdown()
		self.socket.close()
"""		
	def check_threads(self):
		before_count = len( self.threads )
		self.threads = [t for t in self.threads if not t.closed]
		after_count  = len( self.threads )
		if (before_count != after_count):
			self.log( "check_threads() removed %d threads from pool" % (before_count-after_count), level=5 )
		
	def call_on_all_clients(self, function):
		self.check_threads()
		for thread in self.threads:
			function(thread)
"""

class DummyLogger:
	def log(self, str, level=5):
		pass
