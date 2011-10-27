{% set package, java_subpackage = "common", "common" %}
package {{ java_package }};

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class MessageType {

	private String name;
	private int id;
	private ParameterType[] parameters;
	private Map<Integer, MessageType> messagesById = new HashMap<Integer, MessageType>();
	private Map<String, MessageType> messagesByName = new HashMap<String, MessageType>();
	private int messageCount;
	
	
	public MessageType(String name, int id, Object... objects) {
		this.name = name;
		this.id = id;
		List<ParameterType> params = new ArrayList<ParameterType>();
		
		Object o;
		
		for (int i = 0; i < objects.length; i++) {
			o = objects[i];
			if (o instanceof ParameterType) {
				params.add((ParameterType)o);
			} else if (o instanceof MessageType) {
				MessageType mt = (MessageType)o;
				this.messagesById.put(mt.id, mt);
				this.messagesByName.put(mt.name, mt);
			}
		}
		this.messageCount = this.messagesById.size();
		this.parameters = new ParameterType[params.size()];
		for (int i = 0; i < params.size(); i++)
			this.parameters[i] = params.get(i);
	}
	
	public String getName() { return name; }
	public int getId() { return id; }
	public ParameterType[] getParameterTypes() { return parameters; }
	public Map<Integer, MessageType> getMessagesById() { return messagesById; }
	public Map<String, MessageType> getMessagesByName() { return messagesByName; }
	public int getMessageCount() { return messageCount; }
}