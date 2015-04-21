import sys

class DefinedError(RuntimeError):
	pass

class PermanentFailure(DefinedError):
	pass

class ConfigurationError(DefinedError):
	pass

class DataError(DefinedError):
	pass

class ResponseError(DefinedError):
	pass

