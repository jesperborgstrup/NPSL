{% set package, java_subpackage = "server", "server" %}
package {{ java_package }};

import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import {{ java_package_root }}.common.Connection;
import {{ java_package_root }}.common.Logger;

public class Server extends Thread implements Logger {
	
	private String host;
	private int port;
	private Connection connection;
	
	private ServerSocket socket;
	private boolean closed = false;
	
	private List<ClientThread> threads = new ArrayList<ClientThread>();
	
	private SimpleDateFormat logDateFormat = new SimpleDateFormat("dd-MM-yy HH:mm:ss"); 
	private static final int LOG_LEVEL = 5;
	
	public Server(String host, int port, Connection connection) {
		this.host = host;
		this.port = port;
		this.connection = connection;
		
		try {
			this.socket = new ServerSocket(port);
			log( String.format("Server started on %s:%s...", host, port ) , 3);
;		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			closed = true;
		}
	}
	
	@Override
	public void run() {
		this.closed = false;
		Socket clientSocket;
		ClientThread clientThread;
		while (!closed) {
			try {
				clientSocket = socket.accept();
				log( String.format("Client connected %s:%s", clientSocket.getRemoteSocketAddress(), clientSocket.getPort()), 5);
				clientThread = new ClientThread(clientSocket, this, connection);
				threads.add( clientThread );
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
				closed = true;
			}
		}
	}
	
	private void logSingle(String s, int level) {
		String datePrefix = logDateFormat.format( new Date () );
		String out = String.format("%s> %s", datePrefix, s);
		if (level <= LOG_LEVEL) {
			System.out.println(out);
		}
	}
	
	public void log(String s, int level) {
		String[] strings = s.split("\n");
		for (int i=0; i < strings.length; i++)
			logSingle(strings[i], level);
	}
	
	public void log(Exception e) {
		e.printStackTrace();
		/*
		StackTraceElement ste;
		log("An exception ocurred:", 1);
		log(e.getMessage(), 1);
		for (int i=0; i < e.getStackTrace().length; i++) {
			ste = e.getStackTrace()[i];
			log(ste.toString(), 1);
		}*/
	}
	
}
