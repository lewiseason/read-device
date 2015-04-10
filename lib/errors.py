import sys
import click

class DefinedError(RuntimeError):
	pass

class PermanentFailure(DefinedError):
	pass

class ConfigurationError(DefinedError):
	pass

class DataError(DefinedError):
	pass

def handle_exception_normally(exctype, value, traceback):
	if issubclass(exctype, DefinedError):
		click.echo("%s: %s" % (exctype.__name__, value), err=True)
	else:
		# If the exception isn't one of ours, handle it in the default way
		sys.__excepthook__(exctype, value, traceback)

def handle_exception_quietly(exctype, value, traceback):
	# Obviously, if the exception occurs in a thread (which is quite likely)
	# this exit code will never go anywhere.
	sys.exit(255)

def set_exception_handler(quiet):
	if quiet:
		sys.excepthook = handle_exception_quietly
	else:
		sys.excepthook = handle_exception_normally
