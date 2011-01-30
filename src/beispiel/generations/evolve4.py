import zope.component
import zope.interface
from zope.app.component import hooks
from zope.app.zopeappgenerations import getRootFolder
from zope.app.generations.utility import findObjectsProviding
import zc.relation
from zope.dublincore.interfaces import IWriteZopeDublinCore
from zope.dublincore.annotatableadapter import DCkey
from zope.annotation.interfaces import IAnnotations
from zope.app.container.interfaces import INameChooser
import zc.catalog
import zope.app.catalog

from quotationtool.site.interfaces import IQuotationtoolSite
from quotationtool.relation import dump, load
from quotationtool.commentary.interfaces import IComment, ICommentContainer
from quotationtool.commentary.commentcontainer import CommentContainer


def evolve(context):

    root = getRootFolder(context)

    site = None
    for s in findObjectsProviding(root, IQuotationtoolSite):
        site = s
        break
    if site is None: raise Exception('No quotationtool site')
    hooks.setSite(site)

    sm = site.getSiteManager()

    # a container for unified comments was added
    container = site['comments'] = CommentContainer()
    sm.registerUtility(container, ICommentContainer)
    IWriteZopeDublinCore(container).title = u"Comments"
    IWriteZopeDublinCore(container).description = u"""Comments are stored here."""

    # relation catalog has changed because of unified comments
    cat = zope.component.getUtility(
        zc.relation.interfaces.ICatalog,
        context = site)
    cat.removeValueIndex('icommentaboutfigure-figure')
    cat.removeValueIndex('icommentaboutreference-reference')
    cat.addValueIndex(
        IComment['about'],
        dump = dump, load = load,
        name = 'icomment-about')

    
