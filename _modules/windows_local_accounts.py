"""
Handle PowerShell LocalAccounts module use

"""

from logging import getLogger

from salt.exceptions import CommandExecutionError


LOGGER = getLogger(__name__)
__version__ = '0.1.0'
__virtualname__ = 'windows_local_accounts'


def __virtual__():
	"""
	Check PowerShell LocalAccounts module availability
	"""

	if not __salt__['windows_powershell.get_module'](name='Microsoft.PowerShell.LocalAccounts', list_available=True):
		return False, 'PowerShell LocalAccounts module not available'

	return __virtualname__


def get_local_user(name=None, sid=None):
	"""

	:param name:
	:param sid:
	:return:
	"""

	kwargs = {}
	if name is not None:
		kwargs['Name'] = name
	if sid is not None:
		kwargs['SID'] = sid

	return __salt__['windows_powershell.run_from_components']('Get-LocalUser', **kwargs)
