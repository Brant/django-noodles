class FakeRequest(object):
    """
    just provide a few things for testing purposes
    to mimic a request object
    """
    def __init__(self, path):
        self.path = unicode(path)


def write_to_file(filename, content):
    with open(filename, 'a') as f:
        f.write(content)
        f.write("\n")
