{%- set default_sources = {'module' : ['windows', 'management'], 'defaults' : False, 'pillar' : True, 'grains' : []} %}
{%- from "windows/defaults/load_config.jinja" import config as management_ with context %}

{%- if management_.clear_all_logs|default(False) %}

all_logs_cleared: windows_management.all_logs_cleared

{%- endif %}
