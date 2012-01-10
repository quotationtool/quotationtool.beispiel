"""
This file is read whenever a beispiel instance is started. So this is
the right place to wire components together. Here we declare some
classImplements in order to slam some marker interfaces from some
packages on classes of other packages. This way we have views
registered, relation preconditions validate as we want etc.
"""

from zope.interface import classImplements

from quotationtool.figuresng.example import Example
from quotationtool.biblatex.biblatexentry import BiblatexEntry
from quotationtool.commentary.interfaces import ICommentable
from quotationtool.categorization.interfaces import ICategorizable
from quotationtool.quotation.interfaces import IReference

# relation precondition for comments
classImplements(BiblatexEntry, ICommentable)
classImplements(Example, ICommentable)

# marker interface for attribution of categories
classImplements(BiblatexEntry, ICategorizable)
classImplements(Example, ICategorizable)

# relation precondition for quotations
classImplements(BiblatexEntry, IReference)


from quotationtool.search.searcher import QuotationtoolSearchFilter
from quotationtool.figuresng.searcher import IExampleSearchFilter
from quotationtool.bibliography.searcher import IBibliographySearchFilter
from quotationtool.quotation.searcher import IQuotationSearchFilter

classImplements(QuotationtoolSearchFilter, IExampleSearchFilter)
classImplements(QuotationtoolSearchFilter, IBibliographySearchFilter)
classImplements(QuotationtoolSearchFilter, IQuotationSearchFilter)
 

# Workflow

from quotationtool.workflow.interfaces import IHasWorkflowHistory
from quotationtool.workflow.interfaces import IRemovable
from quotationtool.workflow.interfaces import ISubjectOfMessage

classImplements(Example, IHasWorkflowHistory)
classImplements(Example, IRemovable)
classImplements(Example, ISubjectOfMessage)

classImplements(BiblatexEntry, IHasWorkflowHistory)
classImplements(BiblatexEntry, IRemovable)
classImplements(BiblatexEntry, ISubjectOfMessage)

from quotationtool.commentary.comment import Comment
classImplements(Comment, IHasWorkflowHistory)
classImplements(Comment, IRemovable)
classImplements(Comment, ISubjectOfMessage)
