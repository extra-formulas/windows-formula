"""

"""

from pathlib import Path
from logging import getLogger


LOGGER = getLogger(__name__)
__version__ = '0.1.0'


def emptied(name, skip_salt_user=False, skip_system=False):
	"""

	:param name:
	:param skip_salt_user:
	:param skip_system:
	:return:
	"""

	ret = {
		'name': name,
		'result': False,
		'changes': {},
		'comment': '',
	}

	if skip_system:
		system_content = []
	else:
		system_dir = __salt__['reg.read_value']('HKEY_LOCAL_MACHINE', r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment', 'TEMP')
		system_dir = __salt__['cmd.shell'](f'echo {system_dir["vdata"]}')
		system_content = [entry for entry in __salt__['file.readdir'](system_dir) if entry not in ('.', '..')]

	if skip_salt_user:
		user_content = []
	else:
		user_dir = __salt__['reg.read_value']('HKEY_CURRENT_USER', 'Environment', 'TEMP')
		user_dir = __salt__['cmd.shell'](f'echo {user_dir["vdata"]}')
		user_content = [entry for entry in __salt__['file.readdir'](user_dir) if entry not in ('.', '..')]

	if not (system_content + user_content):
		ret['result'] = True
		ret['comment'] = 'Requested temp folders are empty'
	elif __opts__['test']:
		ret['result'] = None
		ret['comment'] = 'Requested temp folders would be emptied'
		if system_content:
			ret['changes'].update({'system': system_content})
		if user_content:
			ret['changes'].update({'user': user_content})
	else:
		deletion_failed = False
		if system_content:
			successes, failures, base_path = [], [], Path(system_dir)
			for entry in system_content:
				try:
					partial = __salt__['file.remove'](str(base_path / entry))
				except Exception:
					failures.append(entry)
				else:
					successes.append(entry)

			result = {}
			if failures:
				deletion_failed = True
				result['failed'] = failures
			if successes:
				result['deleted'] = successes
			ret['changes'].update({'system': result})

		if user_content:
			successes, failures, base_path = [], [], Path(user_dir)
			for entry in user_content:
				try:
					partial = __salt__['file.remove'](str(base_path / entry))
				except Exception:
					failures.append(entry)
				else:
					successes.append(entry)

			result = {}
			if failures:
				deletion_failed = True
				result['failed'] = failures
			if successes:
				result['deleted'] = successes
			ret['changes'].update({'user': result})

		ret['result'] = not deletion_failed
		if deletion_failed:
			ret['comment'] = "Requested temp directories couldn't be emptied"
		else:
			ret['comment'] = 'Requested temp directories were emptied'

	return ret
