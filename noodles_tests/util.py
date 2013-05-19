class FakeRequest(object):
    """
    just provide a few things for testing purposes
    to mimic a request object
    """
    def __init__(self, path):
        self.path = unicode(path)