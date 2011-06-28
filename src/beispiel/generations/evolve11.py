def evolve(context):
    """ split of quotationtool.quotation package

    - add 'iquotation-reference' value index to relation catalog

    - remove 'ifigure-reference' value index form relation catalog

    - index_doc all items in search catalogs and in relation catalog

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

    from z3c.indexer.interfaces import IIndexer
    from z3c.indexer.indexer import index
    
    from quotationtool.figuresng.indexing import createExampleIndices
    from quotationtool.quotation.indexing import createQuotationIndices
    from quotationtool.bibliography.indexer import createBibliographyIndices
    from quotationtool.search import createIndices

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

    relations = zope.component.getUtility(
        zc.relation.interfaces.ICatalog,
        context = site)
    relations.addValueIndex(
        IQuotation['reference'],
        dump=dump, load=load,
        name="iquotation-reference")
    relations.removeValueIndex('ifigure-reference')

    createExampleIndices(site)
    createQuotationIndices(site)
    createBibliographyIndices(site)
    createIndices(site)

    for example in findObjectsProviding(site, IQuotation):
        
        # relations
        relations.index(example)
        
        # page, volume, position
        example.page = example.volume = u""
        pos = example.position
        change = True
        for c in example.position:
            if not c in ('0123456789-/f. Sp'):
                change = False
        if change:
            page = example.position.strip()
            page = page.strip('S.')
            page = page.strip('p.')
            example.page = page.strip()
            example.position = u""
