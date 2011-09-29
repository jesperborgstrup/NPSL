from server import Server
from serverinterface import ServerInterface


if __name__ == "__main__":
	
	s = Server(interface=ServerInterface())
	s.start()