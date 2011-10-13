{% set package, java_subpackage = "common", "common" %}
package {{ java_package }};

public interface Logger {

	public void log(String s, int level);
	public void log(Exception e);
}
