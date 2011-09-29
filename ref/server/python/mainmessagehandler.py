from settings import Settings
from messagehandler import MessageHandler
from modules import modules

class MainMessageHandler(MessageHandler):
	
	def __init__(self, client):
		MessageHandler.__init__(self, client)
		print modules
		
	def handle(self, message):
		state, message = self.parse_struct( message, Settings.STATE_FORMAT )
		module, message = self.parse_struct( message, Settings.MODULE_FORMAT )
		
		if state == None:
			self.log( "No state" )
		else:
			self.log( "State=%d" % state )
			
		if module == None:
			self.log( "No module, error!" )
		else:
			self.log( "Module=%d" % module )
			
		l = {}
		if modules.has_key( module ):
			handlerclass = modules[module].messagehandler
			handler = handlerclass(self.client)
			handler.handle( message )
		else:
			raise RuntimeException( "Unknown module %d" % module )
		
