# Copyright 2015 University of Edinburgh
# Licensed under GPLv3 - see README.md for information

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

