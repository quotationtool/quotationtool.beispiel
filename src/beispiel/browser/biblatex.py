import zope.interface
from z3c.form import validator
from zope.i18n import translate

from quotationtool.biblatex.browser.view import TitleView, YearView
from quotationtool.biblatex.browser.add import AdvancedAddForm
from quotationtool.biblatex.browser.edit import EditPublicationFactsStep
from quotationtool.biblatex import interfaces
from quotationtool.biblatex.interfaces import IBiblatexEntry
from quotationtool.biblatex.ifield import IDate, ILiteral

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
        origyear = getattr(self.context, 'origdate', None)
        if origyear:
            years = IBiblatexEntry['origdate'].extractYears(origyear)
            if years[0] != years[1]:
                i18n_string = _('year-range', u"$lower...$upper",
                                mapping =  {'lower': unicode(years[0]), 
                                            'upper':unicode(years[1])})
                rc += translate(i18n_string, context=self.request) + u" "
            else:
                rc += unicode(years[0]) + u" "
        if origyear:
            casted_years = ()
            for attr in ('date', 'eventdate', 'year'):
                val = getattr(self.context, attr, None)
                if val:
                    if IDate.providedBy(IBiblatexEntry[attr]):
                        casted_years += IBiblatexEntry[attr].extractYears(val)
                    else: 
                        if ILiteral.providedBy(IBiblatexEntry[attr]):
                            try:
                                casted_years += int(val)
                            except Exception:
                                pass
            if not years[0] in casted_years:
                rc += u" (%s)" % super(YearViewBSP, self).__call__().strip()
        else:
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
