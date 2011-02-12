from zope.publisher.browser import BrowserView


class QuotationtoolLabelViewBSP(BrowserView):
    """ A label for the quotationtool app."""

    def __call__(self):
        return u"Archiv des Beispiels"
