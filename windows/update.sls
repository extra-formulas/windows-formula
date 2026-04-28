{%- set default_sources = {'module' : ['windows', 'update'], 'defaults' : True, 'pillar' : True, 'grains' : []} %}
{%- from "windows/defaults/load_config.jinja" import config as update_ with context %}

{%- if update_.clear_cache|default(False) %}

{%- set directories = salt['windows_update.get_cache_content'](*update_.windows_update_cache_directories|default([])) %}

{%- if directories %}
stop_windows_update_service:
  service.dead:
    - name: {{ update_.service_name }}

stop_cryptographic_service:
  service.dead:
    - name: {{ update_.crypt_service_name }}

windows_update_cache_directories:
  windows_update.clean_cache_directories:
    - directories: {{ directories }}
    - require:
      - stop_windows_update_service
      - stop_cryptographic_service

start_cryptographic_service:
  service.running:
    - name: {{ update_.crypt_service_name }}

start_windows_update_service:
  service.running:
    - name: {{ update_.service_name }}
{%- endif %}

{%- endif %}