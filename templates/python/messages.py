{% set output_dest, package = "messages.py", "common" %}

from messagetype import MessageType
from datatypes import DataTypes


{% macro module_macro(name, id, parameters, messages, modules, direction, indent) -%}MessageType(name="{{ name }}",{% filter indent(indent) %}
            id={{ id }},
{% if parameters|length > 0 %}            params=[{% for item in parameters|direction(direction) %}("{{ item.parameter.name }}", {{ item.parameter.type|datatype }}){% if not loop.last %}, {% endif %}{% endfor %}],
{% else %}{% endif %}{% if messages|length > 0 or modules|length > 0 %}            messages={ {% if messages|length > 0 %}
{% for item in messages|direction(direction) %}                      {{ "% 4d"|format(item.id) }}: MessageType({{ "% 4d"|format(item.id) }}, "{{ item.name }}"{% if item.parameters|length > 0 %}, params=[{% for param in item.parameters %}("{{ param.name }}", {{ param.type|datatype }}){% if not loop.last %}, {% endif %}{% endfor %}]{% endif %}),
{% endfor %}{% else %}{% endif %}{% if modules|length > 0 %}{% for module in modules %}{{ "% 4d"|format(module.id) }}: {{ module_macro(module.name, module.id, module.parameters, module.messages, module.modules, direction, indent+16) }}{% endfor %}
{% else %}{% endif %}                     }{% endif %}
           ){% endfilter %}{%- endmacro %}

# Messages from client to server
servermain = {{ module_macro(name, id, parameters, messages, modules, "c2s", 13) }}

# Messages from server to client
clientmain = {{ module_macro(name, id, parameters, messages, modules, "s2c", 13) }}
