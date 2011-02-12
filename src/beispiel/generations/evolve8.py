def evolve(context):
    """ After evolution from 2009 version to 2011 version:

    - register all database items in intids utility in order to get
      them indexed for relation and search catalogs

    - index_doc the items in search catalogs and in relation catalog

    """

    # We moved the imports here because of getInfo which only takes
    # the __doc__ string in evolve. getInfo should not import
    # anything.
    import zope.interface
    import zope.component
    from zope.app.zopeappgenerations import getRootFolder
    from zope.app.generations.utility import findObjectsProviding
    from zope.app.component import hooks
    import zc.relation
    import zope.catalog
    import zope.intid

    from quotationtool.site.interfaces import IQuotationtoolSite


    root = getRootFolder(context)

    site = None
    for s in findObjectsProviding(root, IQuotationtoolSite):
        site = s
        break
    if site is None:
        raise Exception('No quotationtool site!')
    hooks.setSite(site)

    sm = site.getSiteManager()



    # register objects
    intids = zope.component.getUtility(zope.intid.interfaces.IIntIds)
    relations = zope.component.getUtility(
        zc.relation.interfaces.ICatalog,
        context = site)
    bibliography_cat = zope.component.getUtility(
        zope.catalog.interfaces.ICatalog,
        context = site,
        name = 'bibliography')
    example_cat = zope.component.getUtility(
        zope.catalog.interfaces.ICatalog,
        context = site,
        name = 'examples')
    for obj in findObjectsProviding(site, zope.interface.Interface):

        intids.register(obj)
        oid = intids.getId(obj)
        
        relations.index(obj)

        bibliography_cat.index_doc(oid, obj)
        example_cat.index_doc(oid, obj)



        

