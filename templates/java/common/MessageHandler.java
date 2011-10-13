{% set package, java_subpackage = "common", "common" %}
package {{ java_package }};

import java.io.IOException;

public class MessageHandler {
	
	public MessageHandler() {}
	
	public Message handle(ByteArray buffer, MessageType messageType) {
		Object[] params = new Object[messageType.getParameterTypes().length];

		int i = 0;
		
		try {
			for (ParameterType p: messageType.getParameterTypes()) {
				params[i] = buffer.parseType( p.getType() );
				i++;
			}
			Message subMessage = null;
			if ( messageType.getMessagesById().size() > 0 ) {
				i = 0;
				
				int msgId = -1;
					msgId = buffer.parseInt();
				if (messageType.getMessagesById().containsKey(msgId)) {
					MessageType subMessageType = messageType.getMessagesById().get(msgId);
					subMessage = handle(buffer, subMessageType);
				} else {
					throw new RuntimeException( String.format( "Unknown message %d", msgId ) );
				}
			}
			
			Message result = new Message(messageType, params, subMessage);
			return result;
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		return null;
	}

}
