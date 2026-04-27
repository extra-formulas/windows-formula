{%- set default_sources = {'module' : ['windows', 'temp'], 'defaults' : False, 'pillar' : True, 'grains' : []} %}
{%- from "windows/defaults/load_config.jinja" import config as temp_ with context %}

{%- if temp_.empty_all|default(False) %}

temp_folders_emptied: windows_temp.emptied

{%- endif %}
