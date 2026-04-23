"""

"""

from logging import getLogger


LOGGER = getLogger(__name__)
__version__ = '0.1.0'


def all_packages_deprovisioned(name):
	"""

	:param name:
	:return:
	"""

	ret = {
		'name': name,
		'result': False,
		'changes': {},
		'comment': '',
	}

	provisioned_packages = __salt__['windows_appx.get_appx_provisioned_package'](online=True)

	if not provisioned_packages:
		ret['result'] = True
		ret['comment'] = 'No packages provisioned'
	elif __opts__['test']:
		ret['result'] = None
		ret['comment'] = 'Packages would be deprovisioned'
		ret['changes'].update({'to deprovision': [package['PackageName'] for package in provisioned_packages]})
	else:
		successes, failures = [], []
		for package in provisioned_packages:
			try:
				partial = __salt__['windows_appx.remove_appx_provisioned_package'](package_name=package['PackageName'], all_users=True, online=True)
			except Exception:
				failures.append(package['PackageName'])
			else:
				successes.append(package['PackageName'])

		if failures:
			ret['result'] = False
			ret['comment'] = 'Some packages were not uninstalled'
			ret['changes'].update({'failed': failures})
			if successes:
				ret['changes'].update({'success': successes})
		else:
			ret['result'] = True
			ret['comment'] = 'All packages uninstalled'
			ret['changes'].update({'success': successes})

	return ret


def all_packages_uninstalled(name):
	"""

	:param name:
	:return:
	"""

	ret = {
		'name': name,
		'result': False,
		'changes': {},
		'comment': '',
	}

	installed_packages = [package for package in __salt__['windows_appx.get_appx_package'](all_users=True) if not package['NonRemovable']]

	if not installed_packages:
		ret['result'] = True
		ret['comment'] = 'No packages installed'
	elif __opts__['test']:
		ret['result'] = None
		ret['comment'] = 'Packages would be uninstalled'
		ret['changes'].update({'to uninstall': [package['Name'] for package in installed_packages]})
	else:

		successes, failures = [], []

		main_packages = [package for package in __salt__['windows_appx.get_appx_package'](all_users=True, package_type_filter='Main') if not package['NonRemovable']]
		for package in main_packages:
			try:
				partial = __salt__['windows_appx.remove_appx_package'](package['PackageFullName'], all_users=True)
			except Exception:
				failures.append(package['Name'])
			else:
				successes.append(package['Name'])

		installed_packages = [package for package in __salt__['windows_appx.get_appx_package'](all_users=True) if not package['NonRemovable']]
		for package in installed_packages:
			try:
				partial = __salt__['windows_appx.remove_appx_package'](package['PackageFullName'], all_users=True)
			except Exception:
				failures.append(package['Name'])
			else:
				successes.append(package['Name'])

		if failures:
			ret['result'] = False
			ret['comment'] = 'Some packages were not uninstalled'
			ret['changes'].update({'failed': failures})
			if successes:
				ret['changes'].update({'success': successes})
		else:
			ret['result'] = True
			ret['comment'] = 'All packages uninstalled'
			ret['changes'].update({'success': successes})

	return ret