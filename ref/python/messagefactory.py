from datatypes import DataTypes
import struct

class MessageFactory:
	main = None
	parent = None
	params = []
	socket = None
	
	def __init__(self, mainmessage, parent=None, params=[], socket=None):
		self.main = mainmessage
		self.parent = parent
		self.params = params
		self.socket = socket
		
	def __write_type(self, typ, value):
		if typ in ( DataTypes.Byte, DataTypes.Int, DataTypes.Float ):
			return struct.pack(DataTypes.formats[typ], value)
		elif typ == DataTypes.IntList:
			return struct.pack(">I", len( value ) ) + "".join(
				[self.__write_type(DataTypes.Int, i) for i in value]
			)
		elif typ == DataTypes.String:
			encoded = value.encode('utf-8')
			if len( encoded ) >= 2 ** 16:
				raise RuntimeError( "String too long. Max size is %d bytes" % (2 ** 16 - 1) )
			# First two bytes of a string transmission is the length of the encoded string
			return struct.pack( ">H", len( encoded ) ) + encoded
		elif typ == DataTypes.StringList:
			return struct.pack(">I", len( value ) ) + "".join(
				[self.__write_type(DataTypes.String, i) for i in value]
			)
		elif typ == DataTypes.Binary:
			if len( encoded ) >= 2 ** 32:
				raise RuntimeError( "Binary too long. Max size is %d bytes" % (2 ** 32 - 1) )
				return struct.pack( ">I", len( value ) ) + value
		else:
			raise RuntimeError( "Unknown datatype: %s" % typ )
		
	def __wrap(self, subdata):
		params = "".join(
			[self.__write_type(self.main.params[i][1], self.params[i]) for i in range( len( self.main.params ) ) ]
		)
		if self.parent != None:
			id = struct.pack(">I", self.main.id)
			data = id + params
			return self.parent.__wrap(data + subdata)
		else:
			total_length = len( params ) + len( subdata )
			result = struct.pack(">I", total_length) + params + subdata
			if self.socket != None:
				self.socket.send( result )
			else:
				return result
		
	def __call__(self, *params):
		if len( params ) != len( self.main.params ):
			raise TypeError ( "%s expected %d arguments, got %d (%s) (%s)" % (self.main.name, len( self.main.params ), len(params ), self.main.params, params ) )
			
		self.params = params
		
		if len( self.main.messages ) == 0:
			return self.__wrap("")
		else:
			return self
		
	def __getattr__(self, name):
		messages = filter( lambda (k,v): v.name == name, self.main.messages.iteritems() )
		if len( messages ) > 0:
			return MessageFactory( messages[0][1], self )
		else:
			raise AttributeError ("No message named %s" % (name))
		
	def __repr__(self):
		return "<MessageFactory(%s)>" % (self.main.name)