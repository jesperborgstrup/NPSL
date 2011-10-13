{% set package, java_subpackage = "server", "server" %}
package {{ java_package }};

import java.util.Map;

import {{ java_package_root }}.common.Connection;
import {{ java_package_root }}.common.Message;
import {{ java_package_root }}.common.SocketThread;

public class ClientConnection implements Connection {

	@Override
	public void Connected(SocketThread otherEnd) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void Disconnected(SocketThread otherEnd) {
		// TODO Auto-generated method stub
		
	}
	
	private byte volume = 0;

	@Override
	public void Message(SocketThread otherEnd, Map<String, Object> parameters, Message message) {
		System.out.println( String.format( "Received from %s:%s> %s", otherEnd.getHost(), otherEnd.getPort(), message));

		if (message.getName().equals("winamp")) {
			if (message.getSubMessage().getName().equals("set_volume")) {
				volume = (Byte)message.getSubMessage().getParameters().get("Volume");
				otherEnd.disconnect();
			} else if (message.getSubMessage().getName().equals("get_volume")) {
				otherEnd.sendMessage("winamp", "get_volume", volume);
			}
		}
		
	}

}
