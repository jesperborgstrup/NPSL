{% set output_dest, package = "serverinterface.py", "server" %}

class ServerInterface:
	
	volume = 0
	
	def __init__(self):
		pass
	
	def connected(self, otherend):
		print "Connected to %s:%s" % ( otherend.host, otherend.port )
		
	def disconnected(self, otherend):
		print "Disconnected from %s:%s" % ( otherend.host, otherend.port )
		
	def message(self, message, otherend):
		mainparams = message.params
		submessage = message.child
		print submessage
		if submessage.name == "winamp":
			winampmessage = submessage.child
			if winampmessage.name == "get_playlist":
				otherend.send.winamp.get_playlist(["String 1", "String 2", "String 3+4"])
			elif winampmessage.name == "set_volume":
				self.volume = winampmessage.params['Volume']
			elif winampmessage.name == "get_volume":
				otherend.send.winamp.get_volume(self.volume)
