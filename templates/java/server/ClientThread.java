{% set package, java_subpackage = "server", "server" %}
package {{ java_package }};

import java.net.Socket;

import {{ java_package_root }}.common.Connection;
import {{ java_package_root }}.common.Messages;
import {{ java_package_root }}.common.SocketThread;

public class ClientThread extends SocketThread {

	public Server server;
	
	public ClientThread(Socket socket, Server server, Connection connection) {
		super(socket, server, connection, Messages.serverMain, Messages.clientMain);
		this.server = server;
	}
	
}
