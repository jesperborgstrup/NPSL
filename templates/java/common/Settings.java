{% set package, java_subpackage = "common", "common" %}
package {{ java_package }};

public class Settings {

	public static boolean IGNORE_UNKNOWN_MESSAGES = {{ setting_ignore_unknown_messages|literal }};
	
}