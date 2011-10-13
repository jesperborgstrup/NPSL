{% set package, java_subpackage = "client", "client" %}
package {{ java_package }};

import java.util.Map;

import {{ java_package_root }}.common.Connection;
import {{ java_package_root }}.common.Message;
import {{ java_package_root }}.common.SocketThread;

public class ServerConnection implements Connection {

	@Override
	public void Connected(SocketThread otherEnd) {
		// TODO Auto-generated method stub
		System.out.println("Connected");
	}

	@Override
	public void Disconnected(SocketThread otherEnd) {
		System.out.println("Disconnected");
	}
	
	@Override
	public void Message(SocketThread otherEnd, Map<String, Object> parameters, Message message) {
		System.out.println( String.format( "Received from %s:%s> %s", otherEnd.getHost(), otherEnd.getPort(), message));
	}

}
