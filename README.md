Copyright 2015 University of Edinburgh.
Author: Lewis Eason <me@lewiseason.co.uk>

# Roadmap

* [ ] Complete work on `meters` command
* [ ] Write useful man pages
* [ ] Analyse concurrency/performance
* [ ] Packaging? Not hard to bundle in an RPM package, symlink groff files and create `/etc/read_device`

## Installation

*This needs a proper write-up, but to get started:*

### CentOS 6 / Python 2.6

```shell
[leason@vortis read_device]$ yum install libxml2-python libxslt-python libxslt-devel
[leason@vortis read_device]$ pip install read-device pymodbus
[leason@vortis read_device]$ mkdir -p /etc/read_device/{profiles,formatters}
[leason@vortis read_device]$ cat > /etc/read_device/site.xml <<-CONFIG
<?xml version="1.0" encoding="UTF-8"?>
<Site>
</Site>
CONFIG
```

## Building

To build your very own source package (and upload it to a package index), simply:

```shell
[leason@vortis read_device]$ python setup.py sdist register upload
```

## The Small Print

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
