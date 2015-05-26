# Copyright 2015 University of Edinburgh
# Licensed under GPLv3 - see README.md for information

import sys
import threading

from .parser import Parser
from .concurrency import WorkQueue

class BaseProfile(object):
    """!
    A base class for every device profile.

    Provides:
            * enforcement of required_arguments if specified on the subclass
            * lightweight work-queue concurrency methods: #queue and #execute
    """

    configured  = False

    ## List of properties. May be populated during configuration or on-the-fly
    properties  = []

    profile_name = None
    parent_name = None

    type = ''
    product = None
    manufacturer = None


    ## If the device is instantiated with a mutator, this will be populated by factories.ProfileFactory
    mutator = None

    def __init__(self, arguments):
        self._queue = WorkQueue()
        self.args = arguments
        self._enforce_required_arguments()

    def configure(self):
        pass

    def enumerate(self):
        """!
        Subclasses should override this method to gather information from the device.
        Use of #queue and #execute is encouraged.

        If properties are discovered on the fly instead of being configured in advance,
        they should be appended to #properties instead of being returned. In both cases
        set the value of the property using `property.value = ...`
        """
        pass

    def queue(self, target, args=(), name=None):
        """!
        @param[in] target function or method to run
        @param[in] args tuple of arguments to pass to the target
        @param[in] name optional name for the job
        """
        self._queue.append(target, args)

    def execute(self):
        """!
        Bar
        """
        self._queue.execute()

    def to_property(self, data):
        if getattr(self, 'munge'):
            self.munge(data)
        return Property(data)

    def __getattr__(self, key):
        return self.args.get(key)

    def _enforce_required_arguments(self):
        if self.required_arguments and not self.required_arguments.issubset(set(self.args)):
            raise ValueError('Tried to instantiate %s with insufficient/ambiguous arguments.' % self.__class__.__name__)

class Property(object):
    """!
    Represents a property of a device.

    Provides an interface for basic arithmetic transforms. If the property has the 'transform' attribute set, it will
    pass the expression and current raw value to parser.Parser before returning the result.
    """

    populated = False

    def __init__(self, args):
        self.__dict__ = args
        self.parser = Parser()

        if 'value' in args:
            self.populate(args['value'])

    def __getattr__(self, key):
        return None

    def populate(self, value):
        """!
        Store the value in the property.

        @deprecated Use the setter instead: `property.value = ...`
        @param[in] value The raw value of the property
        """
        self.value = value

    @property
    def value(self):
        val = self._value
        if self.populated and self.transform:
            # Use the parser to transform the value, based on
            # a simple math expression.
            val = self.parser.eval(self.transform, { 'value': val })

        return val

    @value.setter
    def value(self, value):
        self.populated = True
        self._value = value
