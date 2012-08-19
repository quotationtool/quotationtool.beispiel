def evolve(context):
    """ evolve workflow components: add worklist-value index
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

    from zope.dublincore.interfaces import IWriteZopeDublinCore
    from quotationtool.workflow.container import WorkFlowContainer
    from quotationtool.workflow.worklist import WorkList
    from quotationtool.workflow import interfaces
    from z3c.indexer.index import SetIndex, ValueIndex
    from z3c.indexer.interfaces import IIndex

    sm['default']['worklist-value'] = idx = ValueIndex()
    sm.registerUtility(idx, IIndex, name='worklist-value')

