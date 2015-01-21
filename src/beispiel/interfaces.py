import zope.interface
from z3c.formui.interfaces import IDivFormLayer
from zope.i18nmessageid import MessageFactory
from zope.viewlet.interfaces import IViewletManager

from quotationtool.skin.interfaces import IQuotationtoolBrowserLayer, IQuotationtoolBrowserSkin


_ = MessageFactory('beispiel')


class IBeispielBrowserLayer(IQuotationtoolBrowserLayer):
    """ The browser layer for the beispiel application inherits the
    quotationtool browser layer."""


class IBeispielBrowserSkin(IBeispielBrowserLayer,
                           IDivFormLayer):
    """ The browser skin for the beispiel application."""


class IRandomExample(zope.interface.Interface):
    """The getExample() method returns randomly picked example. This
    interface may be implemented by nice utilities."""

    def getExample():
        """Returns an example."""


class IFrontpage(IViewletManager):
    """A viewlet manager for the frontpage. """
