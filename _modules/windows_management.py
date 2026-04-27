"""
Handle PowerShell Management module use

"""

from logging import getLogger

from salt.exceptions import CommandExecutionError


LOGGER = getLogger(__name__)
__version__ = '0.1.0'
__virtualname__ = 'windows_management'


def __virtual__():
	"""
	Check PowerShell Management module availability
	"""

	if not __salt__['windows_powershell.get_module'](name='Microsoft.PowerShell.Management', list_available=True):
		return False, 'PowerShell Management module not available'

	return __virtualname__


def clear_event_log(log_name=None, computer_name=None, what_if=False, confirm=False):
	"""

	:param log_name:
	:param computer_name:
	:param what_if:
	:param confirm:
	:return:
	"""

	kwargs = {}
	if log_name is not None:
		kwargs['LogName'] = f'"{log_name}"'
	if computer_name is not None:
		kwargs['ComputerName'] = f'"{computer_name}"'
	if what_if:
		kwargs['WhatIf'] = None
	if confirm:
		kwargs['Confirm'] = None

	return __salt__['windows_powershell.run_from_components']('Clear-EventLog', **kwargs)


def get_event_log(log_name=None, as_base_object=False, computer_name=None, list=False, as_string=False):
	"""

	:param log_name:
	:param computer_name:
	:param list:
	:param as_string:
	:return:
	"""

	kwargs = {}
	if list:
		kwargs['List'] = None
		if as_string:
			kwargs['AsString'] = None
	else:
		if log_name is not None:
			kwargs['LogName'] = log_name
		if as_base_object:
			kwargs['AsBaseObject'] = None

	if computer_name is not None:
		kwargs['ComputerName'] = computer_name

	return __salt__['windows_powershell.run_from_components']('Get-EventLog', **kwargs)