import zope.interface
from z3c.form import validator

from quotationtool.biblatex.browser.view import TitleView, YearView
from quotationtool.biblatex.browser.add import AdvancedAddForm
from quotationtool.biblatex.browser.edit import EditPublicationFactsStep
from quotationtool.biblatex import interfaces
from quotationtool.biblatex.interfaces import IBiblatexEntry

from beispiel.interfaces import IBeispielBrowserLayer, _


class TitleViewBSP(TitleView):
    """ Print 'origtitle' if there is one."""

    def __call__(self):
        rc = u""
        origtitle = getattr(self.context, 'origtitle', u"")
        if origtitle:
            rc += IBiblatexEntry['origtitle'].toUnicode(origtitle)
            return rc
        return super(TitleViewBSP, self).__call__()


class YearViewBSP(YearView):

    def __call__(self):
        rc = u""
        origdate = getattr(self.context, 'origdate', None)
        if origdate:
            rc += IBiblatexEntry['origdate'].toUnicode(origdate) + u" / "
        rc += super(YearViewBSP, self).__call__()
        return rc


class AdvancedAddFormBSP(AdvancedAddForm):
    """The add form with an additional 'origdate' field."""
    
    more_fields = AdvancedAddForm.more_fields + ('origdate', 'origtitle',)

    def updateWidgets(self):
        super(AdvancedAddFormBSP, self).updateWidgets()
        self.widgets['origdate'].required = True
        self.widgets['origtitle'].required = True


class EditPublicationFactsStepBSP(EditPublicationFactsStep):
    """ Wizard step with 'origdate' widget required."""

    def updateWidgets(self):
        super(EditPublicationFactsStepBSP, self).updateWidgets()
        self.widgets['origdate'].required = True
        self.widgets['origtitle'].required = True


class OrigDateRequiredValidator(validator.SimpleFieldValidator):
    """ In the beispiel application we always want the 'origdate'
    field present."""

    def validate(self, value):
        super(OrigDateRequiredValidator, self).validate(value)
        if not value:
            raise zope.interface.Invalid(_(u"No value for 'origdate' provided."))


validator.WidgetValidatorDiscriminators(
    OrigDateRequiredValidator,
    field = IBiblatexEntry['origdate'],
    request = IBeispielBrowserLayer,
    )


class OrigTitleRequiredValidator(validator.SimpleFieldValidator):
    """ In the beispiel application we always want the 'origtitle'
    field present."""

    def validate(self, value):
        super(OrigTitleRequiredValidator, self).validate(value)
        if not value:
            raise zope.interface.Invalid(_(u"No value for 'origtitle' provided."))


validator.WidgetValidatorDiscriminators(
    OrigTitleRequiredValidator,
    field = IBiblatexEntry['origtitle'],
    request = IBeispielBrowserLayer,
    )
