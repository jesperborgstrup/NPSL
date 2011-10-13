{% set package, java_subpackage = "client", "client" %}
package {{ java_package }};

public class ClientRunner {

	/**
	 * @param args
	 * @throws InterruptedException 
	 */
	public static void main(String[] args) throws InterruptedException {
		Client c = new Client("localhost", 1234, new ServerConnection());
		if (!c.connect()) {
			System.out.println("Couldn't connect. Exiting...");
			System.exit(-1);
		}
		c.sendMessage("winamp", "set_volume", (byte)25);
		c.sendMessage("winamp", "get_volume");
		Thread.sleep(200);
		c.disconnect();
		
		// TODO Auto-generated method stub

	}

}
