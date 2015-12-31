from zope.publisher.browser import BrowserView
from z3c.pagelet.browser import BrowserPagelet
import zope.interface
from z3c.pagelet.browser import BrowserPagelet
from zope.viewlet.manager import ViewletManager, WeightOrderedViewletManager
from zope.viewlet.viewlet import ViewletBase
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from z3c.template.interfaces import IContentTemplate

from beispiel import interfaces


class Frontpage(BrowserPagelet):
    """ The frontpage for 'archiv des beispiels'."""

    #zope.interface.implements(interfaces.IStartPagePagelet)


class QuotationtoolLabelViewBSP(BrowserView):
    """ A label for the quotationtool app."""

    def __call__(self):
        return u"Archiv des Beispiels"


class StartPagelet(BrowserPagelet):
    """ A pagelet for the start page. """



FrontpageManager = ViewletManager('frontpage',
                                  interfaces.IFrontpage,
                                  bases = (WeightOrderedViewletManager,))


class IdeePagelet(BrowserPagelet):
    """ A pagelet for the page describing the idea of Archiv des
    Beispiels."""


class Footer(BrowserView):
    """ A view for the footer."""

    def __call__(self):
        template = zope.component.getMultiAdapter((self, self.request), IContentTemplate)
        return template(self)


class ContactPagelet(BrowserPagelet):
    """A pagelet for contact information."""


class ImprintPagelet(BrowserPagelet):
    """A pagelet for imprint information."""

    
