from zope.publisher.browser import BrowserView
from z3c.pagelet.browser import BrowserPagelet
import zope.interface
from z3c.pagelet.browser import BrowserPagelet
from zope.viewlet.manager import ViewletManager, WeightOrderedViewletManager
from zope.viewlet.viewlet import ViewletBase
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

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


class Projects(ViewletBase):
    
    template = ViewPageTemplateFile('projects.pt')
    
    def render(self):
        return self.template()
