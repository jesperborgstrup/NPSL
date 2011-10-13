{% set package, java_subpackage = "common", "common" %}
package {{ java_package }};

{% macro module_macro(name, id, parameters, messages, modules, direction, indent) -%}{% filter indent(indent) %}new MessageType("{{ name }}", {{ id }}, {% if parameters|length > 0 %}{% for item in parameters|direction(direction) %}, new ParameterType("{{ item.parameter.name }}", {{ item.parameter.type|datatype }}){% endfor %}{% endif %}
{% if messages|length > 0 %}{% for item in messages|direction(direction) %}new MessageType("{{ item.name }}", {{ item.id }}{% if item.parameters|length > 0 %}{% for param in item.parameters %}, new ParameterType("{{ param.name }}", {{ param.type|datatype }}){% endfor %}{% endif %}){% if not loop.last %}, 
{% endif %}{% endfor %}{% endif %}{% for module in modules %}{{ module_macro(module.name, module.id, module.parameters, module.messages, module.modules, direction, indent+4 ) }}{% endfor %})
{% endfilter %}{%- endmacro %}
public class Messages {
    // Messages from client to server
    public static MessageType serverMain =
        {{ module_macro(name, id, parameters, messages, modules, "c2s", 8) }};

    // Messages from server to client
    public static MessageType clientMain =
        {{ module_macro(name, id, parameters, messages, modules, "s2c", 8) }};

}
