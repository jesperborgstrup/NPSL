import struct
from datatypes import DataTypes
from settings import Settings
from message import Message

class MessageHandler:
	
	logger = None
	
	def __init__(self, logger):
		self.logger = logger
		
	def handle(self, buffer, messagetype):
		params = {}
		submessage = None
		
		for name, type in messagetype.params:
			params[name], buffer = self.parse_datatype(buffer, type)
		
		if len( messagetype.messages ) > 0:
			msgid, buffer = self.parse_struct( buffer, Settings.MODULE_FORMAT )

			if messagetype.messages.has_key( msgid ):
				submessagetype = messagetype.messages[ msgid ]
				submessage, buffer = self.handle(buffer, submessagetype)
			else:
				raise RuntimeError( "Unknown message %d" % msgid )
			
		message = Message(name=messagetype.name, params=params, child=submessage)
		
		return message, buffer
	
	def parse(self, buffer, length):
		return buffer[:length], buffer[length:]
		
	def parse_struct(self, buffer, format):
		if format == "":
			return None, buffer
		else:
#			try:
				str, buffer = self.parse( buffer, struct.calcsize( format ) )
				return ( struct.unpack( format, str )[0], buffer )
#			except:
#				raise RuntimeError("PARSE")
				
	def parse_datatype_list(self, buffer, datatypes):
		result = []
		for type in datatypes:
			p, buffer = self.parse_datatype(buffer, type)
		
		return result
			
	def parse_datatype(self, buffer, datatype):
		if   datatype == DataTypes.Byte:
			return self.parse_struct(buffer, ">B")
		elif datatype == DataTypes.Int:
			return self.parse_struct(buffer, ">I")
		elif datatype == DataTypes.IntList:
			return self.parse_int_list(buffer)
		elif datatype == DataTypes.Float:
			return self.parse_struct(buffer, ">f")
		elif datatype == DataTypes.String:
			return self.parse_string(buffer)
		elif datatype == DataTypes.StringList:
			return self.parse_string_list(buffer)
		elif datatype == DataTypes.Binary:
			return self.parse_string(buffer)
		else:
			raise RuntimeException("Unknown datatype: %d" % datatype)
			
	def parse_int_list(self, buffer):
		int_count, buffer = self.parse_struct(buffer, ">I")
		result = []
		for i in range(int_count):
			int, buffer = self.parse_struct(buffer, ">I")
			result.append(int)

		return (result, buffer)
		
	def parse_string(self, buffer):
		length, buffer = self.parse_struct(buffer, ">H")
		return self.parse(buffer, length)
		
	def parse_string_list(self, buffer):
		string_count, buffer = self.parse_struct(buffer, ">I")
		result = []
		for i in range(string_count):
			string, buffer = self.parse_string(buffer)
			result.append(string)
			
		return (result, buffer)
		
	
	def log(self, str, level=5):
		return self.logger.log( "Handler> %s" % (str), level)
