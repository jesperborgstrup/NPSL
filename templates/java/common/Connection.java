{% set package, java_subpackage = "common", "common" %}
package {{ java_package }};

import java.util.Map;


public interface Connection {
	
	public void Connected(SocketThread otherEnd);
	public void Disconnected(SocketThread otherEnd, DisconnectReason reason);
	public void Message(SocketThread otherEnd, Map<String, Object> parameters, Message m);

}
