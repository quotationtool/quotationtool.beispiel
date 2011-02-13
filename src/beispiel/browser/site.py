from zope.publisher.browser import BrowserView
from z3c.pagelet.browser import BrowserPagelet


class Frontpage(BrowserPagelet):
    """ The frontpage for 'archiv des beispiels'."""


class QuotationtoolLabelViewBSP(BrowserView):
    """ A label for the quotationtool app."""

    def __call__(self):
        return u"Archiv des Beispiels"
