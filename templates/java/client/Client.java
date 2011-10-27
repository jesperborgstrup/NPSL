{% set package, java_subpackage = "client", "client" %}
package {{ java_package }};

import java.text.SimpleDateFormat;
import java.util.Date;

import java.io.IOException;
import java.net.SocketTimeoutException;
import java.net.UnknownHostException;
import android.util.Log;

import {{ java_package_root }}.client.ConnectException.Reason;
import {{ java_package_root }}.common.Connection;
import {{ java_package_root }}.common.Logger;
import {{ java_package_root }}.common.Messages;
import {{ java_package_root }}.common.SocketThread;

public class Client extends SocketThread implements Logger {

	private String host;
	private int port;
	private int connectTimeout = 2000;
	
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
	public void connect() throws ConnectException {
		// connect() function in SocketThread
		try {
			super.connect(host, port, connectTimeout);
		} catch (IOException e) {
			if (e.getMessage().endsWith("Connection refused")) {
				throw new ConnectException(e, Reason.CONNECTION_REFUSED);
			} else if (e.getMessage().endsWith("Network unreachable")) {
				throw new ConnectException(e, Reason.NETWORK_UNREACHABLE);
			} else if (e.getMessage().endsWith("The operation timed out")) {
				throw new ConnectException(e, Reason.TIMEOUT);
			} else if (e instanceof SocketTimeoutException) {
				throw new ConnectException(e, Reason.TIMEOUT);
			} else if (e instanceof UnknownHostException) {
				throw new ConnectException(e, Reason.UNKNOWN_HOST);
			} else {
				throw new ConnectException(e, Reason.UNKNOWN_REASON);
			}
		}
	}
	
	public void disconnect() {
		super.disconnect();
	}

	private static final String TAG = "mediaplayer_client";
	private void logSingle(String s, int level) {
		String datePrefix = logDateFormat.format( new Date () );
		String out = String.format("%s> %s", datePrefix, s);
		if (level <= LOG_LEVEL) {
			System.out.println(out);
		}
		
		// Logcat
		if (level >= 10)
			Log.v(TAG, s);
		else if (level >= 7)
			Log.d(TAG, s);
		else if (level >= 5)
			Log.i(TAG, s);
		else if (level >= 2)
			Log.w(TAG, s);
		else
			Log.e(TAG, s);
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