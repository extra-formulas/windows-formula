"""

"""

from logging import getLogger


LOGGER = getLogger(__name__)
__version__ = '0.1.0'


def remove_all_accounts(name, skip_accounts=()):
	"""

	:param name:
	:param skip_accounts:
	:return:
	"""

	ret = {
		'name': name,
		'result': False,
		'changes': {},
		'comment': '',
	}

	users_profiles =  __salt__['windows_cim.get_cim_instance']('Win32_UserProfile')
	users_profiles = [user for user in users_profiles if not user['Special']]
	users_profiles = {__salt__['windows_local_accounts.get_local_user'](sid=users_profile['SID'])['Name']: users_profile for users_profile in users_profiles}
	users_profiles = {name: profile for name, profile in users_profiles.items() if name not in skip_accounts}

	if not users_profiles:
		ret['result'] = True
		ret['comment'] = 'No accounts to delete'
	elif __opts__['test']:
		ret['result'] = None
		ret['comment'] = 'Accounts will be deleted'
		ret['changes'].update({'to be deleted': list(users_profiles.keys())})
	else:
		pass

	return ret