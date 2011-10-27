{% set package, java_subpackage = "client", "client" %}
package {{ java_package }};

public class ConnectException extends Exception {
	
	public enum Reason { CONNECTION_REFUSED,
						 NETWORK_UNREACHABLE,
						 TIMEOUT,
						 UNKNOWN_HOST, 
						 UNKNOWN_REASON };

	private static final long serialVersionUID = -7688712833037434454L;
	
	private Reason reason;
	
	public ConnectException( Reason reason ) {
		super();
		this.reason = reason;
	}
	
	public ConnectException( Throwable cause, Reason reason ) {
		super(cause);
		this.reason = reason;
	}
	
	public Reason getReason() {
		return reason;
	}

}
