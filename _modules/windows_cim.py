"""
Handle PowerShell CimCmdlets module use

"""

from logging import getLogger

from salt.exceptions import CommandExecutionError


LOGGER = getLogger(__name__)
__version__ = '0.1.0'
__virtualname__ = 'windows_cim'


def __virtual__():
	"""
	Check PowerShell CimCmdlets module availability
	"""

	if not __salt__['windows_powershell.get_module'](name='CimCmdlets', list_available=True):
		return False, 'PowerShell CimCmdlets module not available'

	return __virtualname__


def get_cim_instance(class_name=None):
	"""

	:param class_name:
	:return:
	"""

	kwargs = {}
	if class_name is not None:
		kwargs['ClassName'] = class_name

	return __salt__['windows_powershell.run_from_components']('Get-CimInstance', **kwargs)


def remove_cim_instance(input_object=None):
	"""

	:param input_object:
	:return:
	"""

	kwargs = {}
	if input_object is not None:
		kwargs['InputObject'] = input_object

	return __salt__['windows_powershell.run_from_components']('Remove-CimInstance', **kwargs)
