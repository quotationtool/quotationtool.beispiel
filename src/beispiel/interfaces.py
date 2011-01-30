import zope.interface


class IRandomExample(zope.interface.Interface):
    """The getExample() method returns randomly picked example. This
    interface may be implemented by nice utilities."""

    def getExample():
        """Returns an example."""
