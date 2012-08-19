def evolve(context):
    """ evolve to categorization based on annotations
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

    root = getRootFolder(context)

    site = None
    for s in findObjectsProviding(root, IQuotationtoolSite):
        site = s
        break
    if site is None:
        raise Exception('No quotationtool site!')
    hooks.setSite(site)

    sm = site.getSiteManager()
    default = sm['default']

    from zope.intid.interfaces import IIntIds
    intids = zope.component.getUtility(IIntIds, context=site)

    from persistent.list import PersistentList
    from z3c.indexer.index import SetIndex
    from z3c.indexer.interfaces import IIndex
    from quotationtool.categorization import interfaces
    from quotationtool.categorization.attribution import ATTRIBUTION_INDEX
    from quotationtool.categorization.relatedattribution import RELATED_ATTRIBUTION_INDEX

    sm['default'][ATTRIBUTION_INDEX] = idx = SetIndex()
    sm.registerUtility(idx, IIndex, name=ATTRIBUTION_INDEX)

    sm['default'][RELATED_ATTRIBUTION_INDEX] = idx = SetIndex()
    sm.registerUtility(idx, IIndex, name=RELATED_ATTRIBUTION_INDEX)

    categories = site['categories']

    # create __categories attribute
    setattr(categories, '_CategoriesContainer__categories', categories._newCategoriesData())

    for catset in categories.values():

        # create relation_indices attribute
        setattr(catset, 'relation_indices', [])

        for name, cat in catset.items():

            # register category in categories container
            categories.addCategory(name, cat)

            # evolve to annotation based attribution
            for intid in cat.attribution:
                obj = intids.getObject(intid)
                attribution = interfaces.IAttribution(obj).attribute(cat.__name__)
                
            # delete integer based attributes of category
            delattr(cat, '_Attribution__attribution')

        # delete integer based attributes of category set
        delattr(catset, '_Attribution__attribution')
