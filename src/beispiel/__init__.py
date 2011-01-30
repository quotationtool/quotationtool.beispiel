"""
This file is read whenever a beispiel instance is started. So this is
the right place to wire components together. Here we declare some
classImplements in order to slam some marker interfaces from some
packages on classes of other packages. This way we have views
registered, relation preconditions validate as we want etc.
"""

from zope.interface import classImplements

from quotationtool.figuresng.example import Example
from quotationtool.figuresng.interfaces import IReference
from quotationtool.biblatex.biblatexentry import BiblatexEntry
from quotationtool.commentary.interfaces import ICommentable
from quotationtool.categorization.interfaces import ICategorizable

# relation precondition for comments
classImplements(BiblatexEntry, ICommentable)
classImplements(Example, ICommentable)

# marker interface for attribution of categories
classImplements(BiblatexEntry, ICategorizable)
classImplements(Example, ICategorizable)

# relation precondition for containing examples (and other figures) 
classImplements(BiblatexEntry, IReference)


# BBB: remove in 0.2.0
from quotationtool.referatory.uniformtitle import UniformTitle
from quotationtool.referatory.reference import Reference
classImplements(Reference, ICommentable)
classImplements(Reference, IReference)
classImplements(UniformTitle, ICategorizable)
classImplements(Reference, ICategorizable)
