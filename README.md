# Usage

* Read the state of a device defined in [config](#Configuration):

  `device enumerate -n '$DEVICE_NAME'`

  *It's possible to enumerate by arguments other than name, by multiple arguments or in a way that matches multiple devices.*

* Read a device on-the-fly/not defined in config (*additional options may be required depending on the profile*):

  `device enumerate -p $PROFILE_NAME -a $DEVICE_ADDRESS`

* List all devices defined in configuration

  `device list`

* Enumerate a device in a different output format

  `device enumerate -n '$DEVICE_NAME' -f cacti`

  *Available formatters are: `pretty` (default), `cacti` and `json`. User-defined formatters may be placed in `/etc/read_device/formatters`*

* List all the device profiles we know about

  `device profiles`

  *User-defined profiles may be placed in `/etc/read_device/profiles`*

* Store the current energy value of all defined electricity meters (*this may take some time*):

  `device -y -f json enumerate -t 'Electricity Meter' | meters store`

# Configuration

Site-specific configuration is done via XML configuration file located at `~/.read_device/site.xml` or
`/etc/read_device/site.xml` and has the following basic structure:

``` xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE Site>
<Site>
  <Device profile="diris.a20" address="172.16.4.1" slave="1" name="TX1" />
  <Device profile="diris.a20" address="172.16.4.2" slave="2" name="TX2" />
</Site>
```

`<Device />` nodes may be placed under intermediary nodes (multiple levels are allowed) to indicate any structure you may
wish to use. The only requirement is that these nodes have a `name` attribute. Here is a fully-featured example:

``` xml
<Site>
  <Building name="ENCOM Tower">
    <Department name="Security">
      <Device profile="diris.a20" address="10.13.0.134" slave="14" name="DB10 Supply" />
    </Department>

    <Department name="Accounting">
      <Device profile="diris.a20" address="10.13.0.134" slave="15" name="DB11 Supply" />
    </Department>

    <Department name="Systems">
      <System name="ENCOM 511">
        <Device profile="malevolent.supercomputer" address="10.13.0.1" slave="humanity" name="ENCOM 511" />
      </System>
    </Department>
  </Building>

  <Building name="Flynn's Arcade">
    <Floor name="Arcade">
      <Device profile="arcade.machine" address="10.13.0.2" name="Time Crisis" />
      <Device profile="arcade.machine" address="10.13.0.3" name="Street Fighter II" />
    </Floor>

    <Floor name="Basement">
      <Device profile="diris.a20" address="10.13.0.134" slave="11" name="TX1" />
      <Device profile="tron" address="10.13.0.221" name="Tron System" />
    </Floor>
  </Building>
</Site>
```

This (contrived) example shows how one might add meaning to a large collection of devices. It's then possible using the
tools provided as part of read-device to interrogate the "location" or "path" of a given device.

> **Technical Bit:** Devices are discovered with the XPath query `//Device` and the location/path is
> discovered by traversing up the tree until no further parents are found.

## Installation

*This needs a proper write-up, but to get started, the following works with the following configuration:*

```shell
[leason@vortis read_device]$ head -n1 /etc/system-release
CentOS release 6.6 (Final)
[leason@vortis read_device]$ python -V
Python 2.6.6
```

```shell
[leason@vortis read_device]$ yum install libxml2-python libxslt-python libxslt-devel
[leason@vortis read_device]$ pip install read-device pymodbus
[leason@vortis read_device]$ mkdir -p /etc/read_device/{profiles,formatters}
[leason@vortis read_device]$ cat > /etc/read_device/site.xml <<-CONFIG
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE Site>
<Site>
</Site>
CONFIG
```

# Glossary

*There are a number of concepts used throughout this documentation and the code to describe various parts of the system
and how they interact. Here are some of them*

**Device**

**Mutator**

**Profile**


# Additional Information

## Roadmap

* [ ] Add definitions to glossary
* [ ] Complete work on `meters` command
* [ ] Write useful man pages?
* [ ] Analyse concurrency/performance
* [ ] Packaging? Not hard to bundle in an RPM package, symlink groff files and create `/etc/read_device`
* [ ] Improved exceptions. Use standard ones more, and write sensible messages

## Building

To build your very own source package (and upload it to a package index), simply:

```shell
[leason@vortis read_device]$ python setup.py sdist register upload
```

## The Small Print

Author: Lewis Eason <me@lewiseason.co.uk>
Copyright 2015 University of Edinburgh.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see [http://www.gnu.org/licenses/].

---

Each file within this program containing the following message:

> Copyright 2015 University of Edinburgh

is part of the read-device project.

A copy of the GNU General Public License can be found in COPYING
