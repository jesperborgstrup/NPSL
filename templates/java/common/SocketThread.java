{% set package, java_subpackage = "common", "common" %}
package {{ java_package }};

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.EOFException;
import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.net.SocketException;

/**
 * Base class for threads reading from and writing to sockets
 * 
 * You 
 * @author jesper
 *
 */
public abstract class SocketThread extends Thread {
	
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
				synchronized (this.socket) { 
					try {
						this.socket.wait();
					} catch (InterruptedException e) {
					}
				}
			}
			if (!closed) {
				try {
					messageLength = in.readInt();
					logger.log( String.format("received message of length %d", messageLength) , 10 );
					buffer = read(messageLength);
					handleMessage( buffer );
				} catch (IOException e) {
					handleException(e);
				}
			}
		}
	}
	
	private void handleMessage(byte[] buffer) {
		Message m = handler.handle(new ByteArray(buffer), receiveMessage);
		connection.Message(this, m.getParameters(), m.getSubMessage());
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
		if (closed)
			return;
		try {
			closed = true;
			socket.close();
			connection.Disconnected(this);
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
				e.getMessage().equalsIgnoreCase( "connection reset" )) {
				disconnect();
			} else if (e.getMessage().equalsIgnoreCase( "broken pipe" )) {
			    logger.log(String.format( "Trying to operate on broken pipe. Closing connection."), 5);
			    disconnect();
} else {
				logger.log(String.format("We have a unhandled SocketException, namely %s", e.getMessage()), 1);
			}
		} else if (e instanceof EOFException) {
			disconnect();
		} else {
			throw new RuntimeException( "Unhandled Exception", e );
		}
		
		
	}

}