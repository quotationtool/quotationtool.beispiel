def evolve(context):
    """ create year-set and origyear-set indices
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
    import zope.intid
    from quotationtool.quotation.interfaces import IQuotation
    from quotationtool.relation import load, dump

    from z3c.indexer.interfaces import IIndexer, IIndex
    from z3c.indexer.index import SetIndex
    
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

    year_set = default['year-set'] = SetIndex()
    origyear_set = default['origyear-set'] = SetIndex()

    sm.registerUtility(origyear_set, IIndex, name='origyear-set')
    sm.registerUtility(year_set, IIndex, name='year-set')

    sm.unregisterUtility(component=default['year-field'], provided=IIndex, name='year-field')
    sm.unregisterUtility(component=default['year-value'], provided=IIndex, name='year-value')
    del default['year-field']
    del default['year-value']


