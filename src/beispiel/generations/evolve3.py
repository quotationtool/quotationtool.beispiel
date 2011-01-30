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
from quotationtool.commentary.aboutfigure import CommentAboutFigureContainer
from quotationtool.commentary.interfaces import ICommentAboutFigureContainer, ICommentAboutReference, ICommentAboutFigure
from quotationtool.referatory.interfaces import IReference
from quotationtool.figuresng.interfaces import IFigure

from quotationtool.figuresng.examplecontainer import ExampleContainer
from quotationtool.figuresng.iexample import IExampleContainer
from quotationtool.figuresng.example import Example
from quotationtool.figuresng.exampleindexing import createExampleIndices, filter
from quotationtool.referatory.indexing import createReferenceIndices

def evolve(context):
    """ restructre form referatory/collectanea/figures to referatory/figuresng.
    relations now live in one single thing."""
    root = getRootFolder(context)

    site = None
    for s in findObjectsProviding(root, IQuotationtoolSite):
        site = s
        break
    if site is None: raise Exception('No quotationtool site')
    hooks.setSite(site)

    sm = site.getSiteManager()

    # a container for comments about figures was added
    container = site['aboutfigures'] = CommentAboutFigureContainer()
    sm.registerUtility(container, ICommentAboutFigureContainer)
    IWriteZopeDublinCore(container).title = u"Comments about Examples"
    IWriteZopeDublinCore(container).description = u"""Comments about examples are stored here."""

    # relation catalog was restructured to one catalog with several indices
    cat = sm['default']['relation_catalog'] = zc.relation.catalog.Catalog(
        dump, load)
    cat.addValueIndex(
        IReference['uniform_title'],
        dump = dump, load = load,
        name = 'ireference-uniform_title')
    cat.addValueIndex(
        IFigure['reference'],
        dump = dump, load = load,
        name = 'ifigure-reference')
    cat.addValueIndex(
        ICommentAboutFigure['figure'],
        dump = dump, load = load,
        name = 'icommentaboutfigure-figure')
    cat.addValueIndex(
        ICommentAboutReference['reference'],
        dump = dump, load = load,
        name = 'icommentaboutreference-reference')
    sm.registerUtility(cat, zc.relation.interfaces.ICatalog)
    for obj in findObjectsProviding(site, IReference):
        cat.index(obj)
    for obj in findObjectsProviding(site, IFigure):
        cat.index(obj)
    for obj in findObjectsProviding(site, ICommentAboutFigure):
        cat.index(obj)
    for obj in findObjectsProviding(site, ICommentAboutReference):
        cat.index(obj)


    # figuresng (figures next generation) need some restructuring

    old_examples = site['examples-g2'] = site['examples']

    site.__delitem__('examples')

    site['examples'] = examples_ng = ExampleContainer()
    sm.registerUtility(examples_ng, IExampleContainer)
    name_chooser = INameChooser(examples_ng)

    extent = zc.catalog.extentcatalog.FilterExtent(filter)
    cat = sm['default']['examples_search_catalog'] = zc.catalog.extentcatalog.Catalog(extent)
    createReferenceIndices(cat)
    createExampleIndices(cat)
    sm.registerUtility(cat, zope.app.catalog.interfaces.ICatalog,
                       name = "examples")

    for old in old_examples.values():
        new = Example()
        new.reference = old.quotation.reference
        new.quotation = unicode(old.quotation.quotation)
        new.source_type = 'quotationtool.figuresng.plaintext'
        new.position = unicode(old.quotation.position)
        new.quid = unicode(getattr(old, 'quid', u""))
        new.pro_quo = unicode(getattr(old, 'pro_quo', u""))
        new.marker = unicode(getattr(old, 'marker', u""))
        name_ = name_chooser.chooseName(new, None)
        examples_ng[name_] = new

        dcdata = IAnnotations(old).get(DCkey)
        annotations = IAnnotations(new)
        annotations[DCkey] = dcdata


