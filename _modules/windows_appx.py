"""
Handle PowerShell Appx module use

"""

from logging import getLogger

from salt.exceptions import CommandExecutionError


LOGGER = getLogger(__name__)
__version__ = '0.1.0'
__virtualname__ = 'windows_appx'


def __virtual__():
	"""
	Check PowerShell Appx module availability
	"""

	if not __salt__['windows_powershell.get_module'](name='Appx', list_available=True):
		return False, 'PowerShell Appx module not available'

	return __virtualname__


def get_appx_package(all_users=False, name=None, package_type_filter=None):
	"""

	:param all_users:
	:return:
	"""

	kwargs = {}
	if all_users:
		kwargs['AllUsers'] = None
	if name is not None:
		kwargs['Name'] = f'"{name}"'
	if package_type_filter is not None:
		kwargs['PackageTypeFilter'] = package_type_filter

	return __salt__['windows_powershell.run_from_components']('Get-AppxPackage', **kwargs)


def get_appx_provisioned_package(online=True):
	"""

	:param online:
	:return:
	"""

	kwargs = {}
	if online:
		kwargs['Online'] = None

	return __salt__['windows_powershell.run_from_components']('Get-AppxProvisionedPackage', **kwargs)


def remove_appx_package(package, /, all_users=False, error_action=None):
	"""

	:param package:
	:param all_users:
	:param error_action:
	:return:
	"""

	kwargs = {
		'Package': package,
	}
	if all_users:
		kwargs['AllUsers'] = None
	if error_action:
		kwargs['ErrorAction'] = error_action

	return __salt__['windows_powershell.run_from_components']('Remove-AppxPackage', **kwargs)


def remove_appx_provisioned_package(package_name=None, all_users=False, online=False, error_action=None):
	"""

	:param package_name:
	:param all_users:
	:param online:
	:param error_action:
	:return:
	"""

	if package_name is not None:
		kwargs = {'PackageName': f'"{package_name}"'}
	else:
		kwargs = {}

	if all_users:
		kwargs['AllUsers'] = None
	if online:
		kwargs['Online'] = None
	if error_action:
		kwargs['ErrorAction'] = error_action

	return __salt__['windows_powershell.run_from_components']('Remove-AppxProvisionedPackage', **kwargs)
