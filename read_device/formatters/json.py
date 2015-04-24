import json

class JSONFormatter:

  def devices(self, devices, **kwargs):
    serialized = [ self._device(device) for device in devices ]
    return json.dumps(serialized, indent=2)

  def _device(self, device):
    data = self._extract_device(device)

    data['path'] = self._path(data.get('path'))
    data['properties'] = map(self._property, data.get('properties'))
    data['properties'] = { prop.get('id'): prop for prop in data['properties'] }

    return data

  def _extract_device(self, device):
    return self._extract_keys(device, [
      'name',
      'address',
      'slave',
      'type',
      'product',
      'properties',
      'path'
      ])

  def _path(self, path):
    return [ (node.tag, node.get('name')) for node in path ]

  def _property(self, property):
    return self._extract_keys(property, [
      'id',
      'name',
      'value',
      'unit',
      ])

  def _extract_keys(self, object, keys):
    """
    Given an object and a list of keys - return a dict of each key getattr'd
    against the object.
    """

    return { attr: getattr(object, attr) for attr in keys }

formatter = JSONFormatter
