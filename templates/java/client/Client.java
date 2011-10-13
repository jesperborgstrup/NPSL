{% set package, java_subpackage = "client", "client" %}
package {{ java_package }};

import java.text.SimpleDateFormat;
import java.util.Date;

import {{ java_package_root }}.common.Connection;
import {{ java_package_root }}.common.Logger;
import {{ java_package_root }}.common.Messages;
import {{ java_package_root }}.common.SocketThread;

public class Client extends SocketThread implements Logger {

	private String host;
	private int port;
	
	private SimpleDateFormat logDateFormat = new SimpleDateFormat("dd-MM-yy HH:mm:ss");
	private static final int LOG_LEVEL = 5;
	
	public Client(String host, int port, Connection connection) {
		/*
		 * The null argument to socket enables us to connect later
		 * with a call to connect().
		 * Due to language restrictions, we cannot directly pass this object
		 * to super() as a Logger, but we have to do it after calling super()
		 */
		super(null, null, connection, Messages.clientMain, Messages.serverMain);
		this.host = host;
		this.port = port;
		this.logger = this;
	}
	
	/**
	 * Try to connect to the hostname and port given upon construction of
	 * the client.
	 * @return True if connected, false otherwise
	 */
	public boolean connect() {
		// connect() function in SocketThread
		return super.connect(host, port);
	}
	
	public void disconnect() {
		super.disconnect();
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
