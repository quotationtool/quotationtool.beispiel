def evolve(context):
    """ Before evolution from 2009 version to 2011 version:

    - It is REQUIRED that you first delete old local utilities by
      hand!

    - create local utilities (relation catalog and search catalogs)

    - register all database items in intids in order to get items
      indexed for relation and search catalogs.

    - clear attributions

    """

    # We moved the imports here because of getInfo which only takes
    # the __doc__ string in evolve. getInfo should not import
    # anything.
    import zope.interface
    import zope.component
    from zope.app.zopeappgenerations import getRootFolder
    from zope.app.generations.utility import findObjectsProviding
    from zope.app.component import hooks

    from quotationtool.site.interfaces import IQuotationtoolSite

    import zc.relation
    import quotationtool.relation
    from quotationtool.figuresng.interfaces import IFigure
    from quotationtool.commentary.interfaces import IComment

    from zope.catalog.interfaces import ICatalog
    from zc.catalog.extentcatalog import FilterExtent, Catalog
    from quotationtool.figuresng import exampleindexing
    from quotationtool.bibliography import indexing as bibliographyindexing
    from quotationtool.figuresng.iexample import IExampleIndexCatalog
    from quotationtool.bibliography.interfaces import IBibliographyCatalog
    from zope.catalog.text import TextIndex

    from quotationtool.categorization.interfaces import IAttributionInjection

    from zope.intid.interfaces import IIntIds
    from quotationtool.bibliography.interfaces import IEntry
    from quotationtool.figuresng.iexample import IExample
    from quotationtool.commentary.interfaces import IComment

    root = getRootFolder(context)

    site = None
    for s in findObjectsProviding(root, IQuotationtoolSite):
        site = s
        break
    if site is None:
        raise Exception('No quotationtool site!')
    hooks.setSite(site)

    sm = site.getSiteManager()


    # relation catalog with indices
    def createRelationCatalog():
        sm['default']['RelationCatalog'] = cat = zc.relation.catalog.Catalog(
            quotationtool.relation.dump, 
            quotationtool.relation.load)
        cat.addValueIndex(
            IFigure['reference'],
            dump = quotationtool.relation.dump,
            load = quotationtool.relation.load,
            name = 'ifigure-reference')
        cat.addValueIndex(
            IComment['about'],
            dump = quotationtool.relation.dump,
            load = quotationtool.relation.load,
            name = 'icomment-about')    
        sm.registerUtility(cat, zc.relation.interfaces.ICatalog)
    createRelationCatalog()


    # example search catalog
    extent = FilterExtent(exampleindexing.filter)#, family = BTrees.family64)
    sm['default']['examples_search_catalog'] = cat = Catalog(extent)
    bibliographyindexing.createBibliographyCatalogIndices(cat)
    exampleindexing.createExampleIndices(cat)
    cat['any'] = TextIndex(
        interface = IExampleIndexCatalog,
        field_name = 'any')
    sm.registerUtility(cat, ICatalog,
                       name = "examples")


    # bibliography search catalog
    extent = FilterExtent(bibliographyindexing.filter)#, family = BTrees.family64)
    sm['default']['bibliography_search_catalog'] = cat = Catalog(extent)
    bibliographyindexing.createBibliographyCatalogIndices(cat)
    cat['any'] = TextIndex(
        interface = IBibliographyCatalog,
        field_name = 'any')
    sm.registerUtility(cat, ICatalog,
                       name = "bibliography")
    


    # clear attributions of categories
    for attribution in findObjectsProviding(site, IAttributionInjection):
        attribution.clearAttribution()

    # register objects
    intids = zope.component.getUtility(IIntIds)
    for obj in findObjectsProviding(site, IEntry):
        intids.register(obj)
    for obj in findObjectsProviding(site, IExample):
        intids.register(obj)
    for obj in findObjectsProviding(site, IComment):
        intids.register(obj)
    for obj in findObjectsProviding(site, IAttributionInjection):
        intids.register(obj)

