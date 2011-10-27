{% set package, java_subpackage = "common", "common" %}
package {{ java_package }};

public enum DisconnectReason {
	BAD_MESSAGE,
	OTHER_END_CLOSED,
	USER,
	UNKNOWN
}
