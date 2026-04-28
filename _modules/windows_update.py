"""
Handle PowerShell Appx module use

"""

from logging import getLogger

from salt.exceptions import CommandExecutionError


LOGGER = getLogger(__name__)
__version__ = '0.1.0'


def get_cache_content(*directories):
	"""

	:param directories:
	:return:
	"""

	directories = [__salt__['cmd.shell'](f'echo {directory}') for directory in directories]
	result = {}
	for directory in directories:
		if __salt__['file.directory_exists'](directory):
			entries = [entry for entry in __salt__['file.readdir'](directory) if entry not in ('.', '..')]
			if entries:
				result[directory] = entries

	return result