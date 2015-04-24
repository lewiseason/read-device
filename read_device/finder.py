class DeviceFinder(object):

  def __init__(self, config):
    self.config = config

  def all(self):
    return self.find()

  def find(self, facets=None):
    """
    Return any devices which match the dictionary of facets passed in
    """
    facets = facets or {}

    # Strip facets which are not defined
    facets = dict([ [k, facets[k]] for k in facets if facets.get(k) ])

    matcher = lambda device: self.match(device, facets)
    return filter(matcher, self.config._devices)

  def create(self, facets=None):
    facets = facets or {}

    profile_name = facets.get('profile')
    profile = self.config.profiles.get(profile_name)

    return self.config.create_device(profile, facets)

  def find_or_create(self, facets):
    matches = list(self.find(facets))

    if matches:
      return matches
    else:
      created = self.create(facets)
      if created:
        return [self.create(facets)]

  def match(self, device, facets):
    """
    Test each facet requested, and if it fails, bail out.
    If the device passes all these facet 'tests' it's a match
    """
    for facet, value in facets.items():
      if getattr(device, facet) != value:
        return False

    return True
