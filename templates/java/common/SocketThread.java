{% set package, java_subpackage = "common", "common" %}
package {{ java_package }};

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.EOFException;
import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.net.SocketException;
import java.net.SocketTimeoutException;

import {{ java_package_root }}.common.MessageHandler.InvalidMessageException;

/**
 * Base class for threads reading from and writing to sockets
 * 
 * You 
 * @author jesper
 *
 */
public abstract class SocketThread extends Thread {
	
	private static final int MESSAGE_READ_TIMEOUT = 5000;
	private Socket socket;
	
	// Logger is protected in order for us to set it after the constructor
	// has been called in Client
	protected Logger logger;
	private Connection connection;
	
	private DataInputStream in;
	private DataOutputStream out;
	private MessageHandler handler = new MessageHandler();
	private MessageFactory messageFactory;
	
	private boolean closed = true;
	
	private MessageType receiveMessage;
	private MessageType sendMessage;
	
	private String host;
	private int port;
	
	public SocketThread(Socket socket, Logger logger, Connection connection,
			MessageType receiveMessage, MessageType sendMessage) {
		this.socket = socket;
		this.logger = logger;
		this.connection = connection;
		this.receiveMessage = receiveMessage;
		this.sendMessage = sendMessage;
		this.messageFactory = new MessageFactory(this.sendMessage);
		
		if (socket != null) {
			try {
				init();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
	}
	
	protected void connect(String host, int port, int timeout) throws IOException {
		if (!closed) {
			return;
		}
		InetSocketAddress isa = new InetSocketAddress(host, port);
		socket = new Socket();
		socket.connect(isa, timeout);
		init();
		
		// If the socket has been disconnected previously, wake up
		// the thread for reading
		synchronized(this) {
			notify();
		}
	}
	
	private void init() throws IOException {
		this.host = socket.getInetAddress().getHostAddress();
		this.port = socket.getPort();
		
		in = new DataInputStream(socket.getInputStream());
		out = new DataOutputStream(socket.getOutputStream());
		connection.Connected(this);
		closed = false;
		if (!this.isAlive())
			start();
	}
	
	public String getHost() { return host; }
	public int getPort() { return port; }
	
	private byte[] read(int length) {
		byte[] result  = new byte[length];
		
		try {
			in.readFully(result, 0, length);
		} catch (IOException e) {
			handleException(e);
		}
		
		return result;
	}
	
	@Override
	public void run() 
		{
		int messageLength;
		byte[] buffer;
		while (true) {
			if (closed) {
				synchronized (this) { 
					try {
						wait();
					} catch (InterruptedException e) {
					}
				}
			}
			if (!closed) {
				try {
					messageLength = in.readInt();
					logger.log( String.format("receiving message of length %d", messageLength) , 10 );
					socket.setSoTimeout( MESSAGE_READ_TIMEOUT );
					try {
						buffer = read(messageLength);
						handleMessage( buffer );
					} catch (Exception e) {
						handleException(e);
					}
					socket.setSoTimeout( 0 );
				} catch (IOException e) {
					handleException(e);
				}
			}
		}
	}
	
	private void handleMessage(byte[] buffer) {
		Message m;
		try {
			m = handler.handle(new ByteArray(buffer), receiveMessage);
			connection.Message(this, m.getParameters(), m.getSubMessage());
		} catch (InvalidMessageException e) {
			handleException(e);
		}
	}
	
	public boolean sendMessage(Object... args) {
		byte[] message = messageFactory.composeMessage(args);
		logger.log( String.format("Sending message of length %d", message.length) , 10 );
		try {
			out.write( message );
			out.flush();
		} catch (IOException e) {
			handleException(e);
			return false;
		}
		return true;
	}
	
	public void disconnect() {
		disconnect(DisconnectReason.USER);
	}
	
	private void disconnect(DisconnectReason reason) {
		if (closed)
			return;
		try {
			closed = true;
			socket.close();
			connection.Disconnected(this, reason);
		} catch (IOException e) {
			// We don't care about exceptions when closing the socket
		}		
	}
	
	protected void handleException(Exception e) {
/*
		if (e.getMessage().equals( "Connection reset" ) ) {
			logger.log( String.format( "Other end quit (%s)", socket.getRemoteSocketAddress()), 5 );
			disconnect();
			return;
		}
		closed = true;
		logger.log(e);
*/
		if (e instanceof SocketException) {
			if (e.getMessage().equalsIgnoreCase( "socket closed" ) ||
				e.getMessage().equalsIgnoreCase( "connection reset" ) ||
				e.getMessage().equalsIgnoreCase( "broken pipe" )) {
				disconnect(DisconnectReason.OTHER_END_CLOSED);
			} else {
				disconnect(DisconnectReason.UNKNOWN);
				logger.log(String.format("We have a unhandled SocketException, namely %s", e.getMessage()), 1);
			}
		} else if (e instanceof EOFException) {
			disconnect(DisconnectReason.OTHER_END_CLOSED);
		} else if (e instanceof InvalidMessageException) {
			disconnect(DisconnectReason.BAD_MESSAGE);
		} else if (e instanceof SocketTimeoutException) {
			disconnect(DisconnectReason.BAD_MESSAGE);
		} else {
			throw new RuntimeException( "Unhandled Exception", e );
		}
		
		
	}

}