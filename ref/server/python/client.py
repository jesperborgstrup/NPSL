import socket, struct
import StringIO
from settings import Settings

def client():
	HOST = 'localhost'    # The remote host
	PORT = 1234       # The same port as used by the server
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	sub = create_sub_package( 100, 150 )
	pkg = create_package( 42, sub )
	s.send( pkg )
	s.close()
#	print 'Received', repr(data)

def create_package(state, sub_package):
	s = StringIO.StringIO()
	sub_length = len( sub_package )
	length = sub_length + 4
	s.write( struct.pack ( Settings.PREFIX_LENGTH_FORMAT, length ) )
	s.write( struct.pack ( Settings.STATE_FORMAT, state ) ) # State 42
	s.write( sub_package )
	result = s.getvalue()
	s.close()
	print "LENGTH=%d, sent=%d" % (len(result), length)
	return result

def create_sub_package(module, message):
	s = StringIO.StringIO()
	s.write( struct.pack( Settings.MODULE_FORMAT, module) )
	s.write( struct.pack( ">I", message) )
	result = s.getvalue()
	s.close()
	print "LENGTHSUB=%d" % len(result)
	return result	

def send_winamp_package(stringio, message_type):
	stringio.write( struct.pack( ">I", 16 ) ) # Packet is 16 bytes long + 4 bytes length prefixed
	stringio.write( struct.pack( ">I", 42 ) ) # State (4 bytes)
	stringio.write( struct.pack( ">I", 100) ) # Module 100 (winamp)

if __name__ == "__main__":
	client()
	
