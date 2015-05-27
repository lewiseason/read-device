# Architecture

`read-device` is made up of a number of python modules under the read_device package.
There is a degree of coupling, but it's fairly easy to follow how they interact.

They are as follows (roughly in order of invocation/use):

## commands

Provides command-line utilities. When you run the `device` or `meters` commands,
this module provides the "entry points" for these utilities.

> Read more about setuptools' entry_points in the [documentation][entry-points].

They parse the input on the command line and interact with other modules to
satisfy the request.

## config

The config module has several functions all relating to configuration and application
state/persistance. It deals with loading the config file, discovering all
available formatters, and caching device entries specified in configuration.

Also available is an interface for searching and interrogating devices. You can
see examples of this in `commands` with methods like `config.devices.find_or_create`.

The application is configured with an XML config file, and an sqlite database
is used for data persistence (in the `meters` script).

### finder

This module provides the aforementioned `find_or_create` lookups. It's quite a simple
module which extends `config`. It doesn't do anything groundbreaking, but looking
at the doxygen docs might be useful if you plan to extend a command.

### factories

*As in the [pattern][factories], not the manufacturing plant variety.*

`factories` provides the following factory classes:

**ProfileFactory**

The main purpose of `ProfileFactory` is to take a profile name and resolve it
to a python class with actual functionality (for example: connecting to a
networked device and retrieving some information).

There may be intermediary steps between the profile name and its class called
"mutators". The purpose of which is to have a flexible base class which accepts
various arguments without repeating them in the config file.

> For more information and an example see [mutators].

**DeviceFactory**

`DeviceFactory` is responsible for creating instances of profiles for specific
devices. It's then possible to query the state of the device (for example, in a
command).

There are two ways a device can be instantiated:

* **Configuration:** devices defined in the configuration file are discovered
with the `from_config` method and cached for searching/querying

* **Arguments:** a device can be instantiated on the fly (`from_arguments`) if
you specify a profile and enough arguments that the profile "knows what to do".

  This allows commands to query devices without a change to the confiruation file
being required. The `device` command makes use of this to allow querying any
known device, not just the ones in the config file.

**FormatterFactory**

Resolves a formatter name to a python class with functionality. Similar to
`ProfileFactory`, but for formatters.

## profiles

All the concrete base classes used by `ProfileFactory` are part of this module.

There is a certain amount of functionality required of each, but the easiest way
to get started is probably to have a look at how the existing ones work.

In the directory with these profiles, you'll see various xml files. These are
[mutators].

## formatters

Commands may have multiple formats they can return their output in. This is to
make the potentially large amount of data human/machine readable without
additional effort.

Again, there is no formal interface for a formatter, but they do all implement
certain methods in common. Go take a look.

---

*Modules still in need of writing up:*

* database - provides data modelling
* decoders - decodes raw data into numbers
* decorators - keep business logic away from plumbing
* parser - parse simple math expressions
* resources - special property class + device class for subclassing
* concurrency
* helpers

---

Inline documentation is scattered throughout the source code and can be turned into
an html API manual with [Doxygen](http://www.doxygen.org/) (which you'll need to install).

In the project directory, run the `doxygen` command and take a look at `doc/html/index.html`.

[mutators]: mutators.md
[entry-points]: https://pythonhosted.org/setuptools/setuptools.html#automatic-script-creation
[factories]: https://en.wikipedia.org/wiki/Factory_(object-oriented_programming)
