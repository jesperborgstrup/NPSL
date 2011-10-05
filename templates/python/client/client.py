import socket, messages
from socketthread import SocketThread

class Client(SocketThread):
	
	host = None
	port = None
	socket = None
	handler = None
	interface = None
	send = None
	logger = None

	def __init__(self, host='localhost', port=1234, interface=None, logger=None):
		socketAddr = (socket.socket(socket.AF_INET, socket.SOCK_STREAM), (host, port))
		SocketThread.__init__(self,
							  socketAddr=socketAddr,
							  interface=interface,
							  logger=logger,
							  recvmessage=messages.clientmain,
							  sendmessage=messages.servermain)
		
	def connect(self):
		try:
			self.socket.connect((self.host, self.port))
			self.start()
		except socket.error, (value, message):
			self.socket_error(value, message)
			
	def disconnect(self):
		if self.socket is None:
			return
		self.shutdown()

	def log(self, str, level=5):
		if level <= 5:
			print str
			