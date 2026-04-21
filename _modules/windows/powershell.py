"""
Handle Powershell use

"""

from logging import getLogger


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
		:rtype: object
		"""

		command_line = self._commands.join(' | ')
		if 'progresspreference' not in command_line.lower():
			command_line = f"$ProgressPreference='SilentlyContinue';{command_line}"
		if 'convertto-json' not in command_line.lower():
			command_line = f"{command_line} | ConvertTo-Json"

		result = __salt__('cmd.run_all')(command_line, shell='powershell', cwd=cwd)

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

def my_test(my_cmd):
	cmd = PowerShellCommand(my_cmd)
	return cmd()
