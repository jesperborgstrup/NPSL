{% set package, java_subpackage = "common", "common" %}
package {{ java_package }};

import java.util.HashMap;
import java.util.Map;

public class Message {
	
	private MessageType type;
	private Map<String, Object> parameters = new HashMap<String, Object>();
	private Message subMessage = null;
	
	public Message(MessageType type, Object[] parameters, Message subMessage) {
		this.type = type;
		if (type.getParameterTypes().length != parameters.length) {
			throw new RuntimeException( String.format( "MessageType %s expected %d parameters, but got %d!", type.getName(), type.getParameterTypes().length, parameters.length ) );
		}
		for (int i = 0; i < parameters.length; i++)
			this.parameters.put( type.getParameterTypes()[i].getName(), parameters[i] );
		
		this.subMessage = subMessage;
	}
	
	public MessageType getType() { return type; }
	public String getName() { return type.getName(); }
	public Map<String, Object> getParameters() { return parameters; }
	public Message getSubMessage() { return subMessage; }
	public boolean hasSubMessage() { return subMessage != null; }
	
	public String toString() {
		String out = String.format( "Message(name=%s, id=%d", type.getName(), type.getId());
		if (parameters.size() > 0)
			out += String.format( ", parameters=%s", parameters);
		if (subMessage != null)
			out += String.format( ", subMessage=%s", subMessage);
		out += ")";
		return out;
	}

}
