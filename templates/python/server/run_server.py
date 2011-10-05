from server import Server
from serverinterface import ServerInterface

class Logger:
	def log(self, str, level=5):
		if level <= 5:
			print str

if __name__ == "__main__":
	
	s = Server(interface=ServerInterface(), logger=None)
	s.start()