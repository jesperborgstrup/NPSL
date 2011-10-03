from .messagetype import MessageType
from .datatypes import DataTypes

# Messages from client to server
servermessages = { 10: MessageType(10,  "set_volume",   params=[("Volume", DataTypes.Byte)]),
				   20: MessageType(20,  "get_volume"),
		          150: MessageType(150, "get_playlist")}

# Messages from server to client
clientmessages = { 20: MessageType(20,  "get_volume",   params=[("Volume", DataTypes.Byte)]),
		          150: MessageType(150, "get_playlist", params=[("Tracks", DataTypes.StringList)])}