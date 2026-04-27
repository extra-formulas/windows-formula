"""

"""

from logging import getLogger


LOGGER = getLogger(__name__)
__version__ = '0.1.0'


def all_logs_cleared(name):
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

	event_logs = __salt__['windows_management.get_event_log'](list=True)
	event_logs_entries = {event_log['Log']: len(event_log['Entries']) for event_log in event_logs}

	if not sum(event_logs_entries.values()):
		ret['result'] = True
		ret['comment'] = 'No log entries to clean'
	elif __opts__['test']:
		ret['result'] = None
		ret['comment'] = 'Log entries would be cleared'
		ret['changes'].update(event_logs_entries)
	else:
		cleared, failures, skipped = [], [], []
		for event_log, count in event_logs_entries.items():
			if count:
				try:
					partial = __salt__['windows_management.clear_event_log'](log_name=event_log)
				except Exception:
					failures.append(event_log)
				else:
					cleared.append(event_log)
			else:
				skipped.append(event_log)

		if failures:
			ret['result'] = False
			ret['comment'] = 'Some logs were not cleared'
			ret['changes'].update({'failed': failures})
			if cleared:
				ret['changes'].update({'cleared': cleared})
		else:
			ret['result'] = True
			ret['comment'] = 'All logs were cleared'
			ret['changes'].update({'cleared': cleared})

		if skipped:
			ret['changes'].update({'skipped': skipped})

	return ret
