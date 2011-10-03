from messagetype import MessageType
from datatypes import DataTypes
import modules.winamp

# Messages from client to server
servermain    = MessageType(name="Main",
							id=-1,
#							params=[("State", DataTypes.Int)],
							messages={100: MessageType(100, "winamp", messages=modules.winamp.servermessages)}
							)

# Messages from server to client
clientmain    = MessageType(name="Main",
							id=-1,
							messages={100: MessageType(100, "winamp", messages=modules.winamp.clientmessages)}
							)
