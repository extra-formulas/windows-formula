{%- set default_sources = {'module' : ['windows', 'appx'], 'defaults' : False, 'pillar' : True, 'grains' : []} %}
{%- from "windows/defaults/load_config.jinja" import config as appx with context %}

{%- if appx.remove_all|default(False) %}

deprovision_all_appx: windows_appx.all_packages_deprovisioned

uninstall_all_appx:
  windows_appx.all_packages_uninstalled:
    - require:
      - deprovision_all_appx

{%- endif %}
