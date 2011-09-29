﻿import socket
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
	
	def __init__(self, host='', port=1234, interface=None):
		threading.Thread.__init__(self)
		self.port = port
		self.host = host
		self.interface = interface
		self.default_encoding = locale.getdefaultlocale()[1]
		
	def run(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind((self.host,self.port))
		self.socket.listen(self.backlog)
		self.log( "Server started on %s:%d" % (self.host, self.port), 2 )
		
		while 1:
			try:
				thread = ClientThread( self, self.socket.accept() )
				self.threads.append( thread )
				thread.start()
			except Exception:
				self.log_exception()
				
	def log(self, str, level=5):
		if level <= 6:
			print str
		
	def log_exception(self):
		exc_type, exc_value, exc_traceback = sys.exc_info()
		lines = traceback.format_exception( exc_type, exc_value, exc_traceback )
		self.log("=== AN EXCEPTION OCCURED ===", level=1)
		[self.log(line.decode( self.default_encoding ), level=1) for line in lines]

	def stop(self):
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