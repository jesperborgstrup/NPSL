{% set output_dest, package = "run_client.py", "client" %}

from client import Client
from clientinterface import ClientInterface

class Logger:
	def log(self, str, level=5):
		if level <= 5:
			print str

if __name__ == "__main__":
	c = Client(port=1234, interface=ClientInterface(), logger=Logger())
	c.connect()
	c.send.winamp.set_volume(25)
	c.send.winamp.get_volume()
	c.disconnect()
	#client()
