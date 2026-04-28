"""

"""

from logging import getLogger
from pathlib import Path


LOGGER = getLogger(__name__)
__version__ = '0.1.0'


def clean_cache_directories(name, directories):
	"""

	:param name:
	:param directories:
	:return:
	"""

	ret = {
		'name': name,
		'result': False,
		'changes': {},
		'comment': '',
	}

	existing = __salt__['windows_update.get_cache_content'](*directories)

	if (not existing) or not sum(existing.values(), []):
		ret['result'] = True
		ret['comment'] = 'No cache content to clean'
	elif __opts__['test']:
		ret['result'] = None
		ret['comment'] = 'Cached files would be cleared'
		ret['changes'].update(existing)
	else:
		total_successes, total_failures = {}, {}
		for directory, content in existing.items():
			successes, failures = [], []
			directory_path = Path(directory)
			for entry in content:
				try:
					partial = __salt__['file.remove'](str(directory_path / entry))
				except Exception:
					failures.append(entry)
				else:
					successes.append(entry)

			if successes:
				total_successes.update({directory: successes})
			if failures:
				total_failures.update({directory: failures})

		if total_failures:
			ret['result'] = False
			ret['comment'] = 'Failed to clear some cached files'
			ret['changes'].update({'failed': total_failures})
			if total_successes:
				ret['changes'].update({'success': total_successes})
		else:
			ret['result'] = True
			ret['comment'] = 'All cached files were cleared'
			ret['changes'].update({'success': total_successes})

	return ret