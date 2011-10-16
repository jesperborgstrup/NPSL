{#{% set package, java_subpackage = "server", "server" %}
    package {{ java_package }};#}

public class ServerRunner {
	public static void main(String[] args) {
		Server s = new Server(null, 1234, new ClientConnection());
		s.start();
	}
}
