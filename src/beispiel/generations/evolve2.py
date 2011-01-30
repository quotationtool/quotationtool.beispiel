import zope.component
from zope.app.component import hooks
from zope.app.zopeappgenerations import getRootFolder
from zope.app.generations.utility import findObjectsProviding
import zc.relation
from zope.dublincore.interfaces import IWriteZopeDublinCore

from quotationtool.site.interfaces import IQuotationtoolSite
from quotationtool.commentary.aboutreference import CommentAboutReferenceContainer, dump, load
from quotationtool.commentary.interfaces import ICommentAboutReferenceContainer, ICommentAboutReference


def evolve(context):
    """ Add a commentary folder and its relation catalog."""
    root = getRootFolder(context)

    site = None
    for s in findObjectsProviding(root, IQuotationtoolSite):
        site = s
        break
    if site is None: raise Exception('No quotationtool site')
    hooks.setSite(site)

    sm = site.getSiteManager()
    
    container = site['aboutreferences'] = CommentAboutReferenceContainer()
    sm.registerUtility(container, ICommentAboutReferenceContainer)
    
    IWriteZopeDublinCore(container).title = u"Comments about References"

    IWriteZopeDublinCore(container).description = u"""Comments about references in the referatory are stored here."""

    
    cat = sm['default']['commentaboutreference_relation_catalog'] = zc.relation.catalog.Catalog(
        dump, load)
    cat.addValueIndex(
        ICommentAboutReference['reference'],
        dump, load)
        
    sm.registerUtility(cat, zc.relation.interfaces.ICatalog,
                       name = 'commentsaboutreferences')
1
