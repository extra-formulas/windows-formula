"""
Handle PowerShell use

"""

from json import loads as json_loads
from logging import getLogger

from salt.exceptions import CommandExecutionError


LOGGER = getLogger(__name__)
__version__ = '0.1.0'
__virtualname__ = 'windows_powershell'


def __virtual__():
	"""
	Check PowerShell availability
	"""

	shell_info = __salt__['cmd.shell_info'](shell='powershell', list_modules=False)
	if not shell_info['installed']:
		return False, 'PowerShell not available'

	return __virtualname__


class PowerShellCommand:
	"""
	Describes a piped command chain for PowerShell.
	"""

	def __call__(self, cwd=None):
		"""Execute the command
		Joins the command with the pipes, runs it in PowerShell and returns the result.

		:return: the result of the command
		:rtype: dict
		"""

		command_line = ' | '.join(self._commands)
		if 'progresspreference' not in command_line.lower():
			command_line = f"$ProgressPreference='SilentlyContinue';{command_line}"
		if 'convertto-json' not in command_line.lower():
			command_line = f"{command_line} | ConvertTo-Json"

		result = __salt__['cmd.run_all'](command_line, shell='powershell', cwd=cwd)

		if 'pid' in result:
			del result['pid']

		if error := result.get('stderr', ''):
			error = error.splitlines()[0]
			raise CommandExecutionError(error, info=result)

		if ('retcode' not in result) or result['retcode']:
			raise CommandExecutionError('Unsuccessful execution of PowerShell command', info=result)

		try:
			result = json_loads(result['stdout'] or '{}', strict=False)
		except ValueError:
			raise CommandExecutionError('Malformed result from PowerShell command', info=result)

		return result

	def __init__(self, initial_command_line):
		"""Initialization
		Add the initial/unique command line to the list of commands in the pipe list

		:param initial_command_line: The initial command line
		:type initial_command_line: str
		"""

		self._commands = [initial_command_line]

	def __or__(self, next_command):
		"""Add a command to the pipe list
		Just adds the provided command line to the list

		:param next_command: the next command to add to the pipe list
		:type next_command: str
		:return: self
		:rtype: PowerShellCommand
		"""

		self._commands.append(next_command)
		return self

	@staticmethod
	def build_command_line(command, /, **kwargs):
		"""

		:param command:
		:param kwargs:
		:return:
		"""

		result = [command]
		for key, value in kwargs.items():
			if value is None:
				result.append(f'-{key}')
			else:
				result.append(f'-{key} {value}')

		return ' '.join(result)

	@classmethod
	def from_components(cls, command, /, **kwargs):
		"""

		:param command:
		:param kwargs:
		:return:
		"""

		return cls(cls.build_command_line(command, **kwargs))


def get_module(name=None, list_available=False):
	"""

	:param name:
	:param list_available:
	:return:
	"""

	if name is None:
		kwargs = {}
	else:
		kwargs = {'Name': f'"{name}"'}

	if list_available:
		kwargs['ListAvailable'] = None

	return run_from_components('Get-Module', **kwargs)


def run_command(command_string):
	"""Run a single liner
	Provided a PowerShell command as a single liner, run it using the PowerShellCommand class.

	:param command_string: the one-liner command to run
	:type command_string: str
	:return: the ultimate result of cmd.run_all
	:rtype: dict
	"""

	cmd = PowerShellCommand(command_string)
	return cmd()


def run_from_components(name, /, **kwargs):
	"""

	:param name:
	:param kwargs:
	:return:
	"""

	cmd = PowerShellCommand.from_components(name, **kwargs)
	return cmd()
