from messagefactory import MessageFactory
from socketthread import SocketThread
import messages


class ClientThread( SocketThread ):
	server = None
	send = None
	
	def __init__(self, socketAddr, server, logger=None):
		SocketThread.__init__(self,
							  socketAddr=socketAddr,
							  interface=server.interface,
							  logger=None,
							  recvmessage=messages.servermain,
							  sendmessage=messages.clientmain)
		self.server = server
		
		self.log( "Connected", level=4 )
		
