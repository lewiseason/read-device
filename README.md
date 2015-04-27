# Installation

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
