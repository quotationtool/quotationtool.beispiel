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
from quotationtool.categorization.interfaces import ICategorizableItemDescriptions, ICategoriesContainer
from quotationtool.categorization.categorizableitemdescription import CategorizableItemDescriptions
from quotationtool.categorization.categoriescontainer import CategoriesContainer


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
    categorizable_items = site['categorizableitems'] = CategorizableItemDescriptions()
    sm.registerUtility(categorizable_items, ICategorizableItemDescriptions)
    IWriteZopeDublinCore(categorizable_items).title = u"Categorizable Item Descriptions"
    IWriteZopeDublinCore(categorizable_items).description = u"""Mapping of ZOPE-Interfaces to user friendly identifiers."""

    categories = site['categories'] = CategoriesContainer()
    sm.registerUtility(categories, ICategoriesContainer)
    IWriteZopeDublinCore(categorizable_items).title = u"Categories"
    IWriteZopeDublinCore(categorizable_items).description = u"""User defined categories for classifying user content."""
    
