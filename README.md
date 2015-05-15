Author: Lewis Eason <me@lewiseason.co.uk>

# The Small Print

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

# Installation

*This needs a proper write-up, but to get started:*

## CentOS 6 / Python 2.6

```shell
yum install libxml2-python libxslt-python libxslt-devel
pip install read-device pymodbus
mkdir -p /etc/read_device/{profiles,formatters}
cat > /etc/read_device/site.xml <<-CONFIG
<?xml version="1.0" encoding="UTF-8"?>
<Site>
</Site>
CONFIG
```
