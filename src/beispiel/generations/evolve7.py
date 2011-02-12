def evolve(context):
    """ Evolve data from the 2009 version to 2011 version.

    - create bibliography
    
    - create biblatex entries from references

    - let examples point to new entry objects

    - grant 'quotationtool.Creator' role to dc.creators[0] of
      examples, comments and entries.

    """


    # We moved the imports here because of getInfo which only takes
    # the __doc__ string in evolve. getInfo should not import
    # anything.
    from zope.app.zopeappgenerations import getRootFolder
    from zope.app.generations.utility import findObjectsProviding
    from zope.app.component import hooks
    from zope.dublincore.interfaces import IWriteZopeDublinCore
    from zope.securitypolicy.interfaces import IPrincipalRoleManager
    from zope.dublincore.annotatableadapter import DCkey
    from zope.annotation.interfaces import IAnnotations
    from zope.app.container.interfaces import INameChooser

    from quotationtool.site.interfaces import IQuotationtoolSite
    from quotationtool.figuresng.iexample import IExample
    from quotationtool.commentary.interfaces import IComment
    from quotationtool.bibliography.bibliography import Bibliography
    from quotationtool.bibliography.interfaces import IBibliography
    from quotationtool.biblatex.biblatexentry import BiblatexEntry

    from quotationtool.referatory.interfaces import IReference
    from quotationtool.referatory.bibtex.iarticle import IArticle
    from quotationtool.referatory.bibtex.ibook import IBook
    from quotationtool.referatory.bibtex.iincollection import IIncollection

    root = getRootFolder(context)

    site = None
    for s in findObjectsProviding(root, IQuotationtoolSite):
        site = s
        break
    if site is None:
        raise Exception('No quotationtool site!')
    hooks.setSite(site)

    sm = site.getSiteManager()

    # grant quotationtool.Creator to the principal who created the
    # object. The principal must be therefor looked up in dc
    # annotation.
    def grantCreator(obj):
        dc = IWriteZopeDublinCore(obj)
        role_manager = IPrincipalRoleManager(obj)
        role_manager.assignRoleToPrincipal(
            'quotationtool.Creator',
            dc.creators[0])
        
        
    # create bibliography
    site['bibliography'] = bibliography = Bibliography()
    sm.registerUtility(bibliography, IBibliography)
    IWriteZopeDublinCore(bibliography).title = u"Bibliography"

    # create new catalogs

    # create biblatex entries form old references
    namechooser = INameChooser(bibliography)
    map = {}
    for reference in findObjectsProviding(site, IReference):
    
        entry = BiblatexEntry()
    
        au = getattr(reference, 'author', ())
        if au:
            entry.author = list(au)
        ed = getattr(reference, 'editor', ())
        if ed:
            entry.editor = list(ed)
        titles = getattr(reference, 'title', ())
        if len(titles) >= 1:
            entry.title = titles[0]
        if len(titles) > 1:
            entry.subtitle = titles[1]
            if len(titles) > 2:
                entry.subtitle += u". " + titles[2]
        entry.publisher = getattr(reference, 'publisher', None)
        entry.date = getattr(reference, 'year', None)
        entry.volume = getattr(reference, 'volume', None)
        entry.number = getattr(reference, 'number', None)
        entry.series = getattr(reference, 'series', None)
        entry.location = getattr(reference, 'address', None)
        entry.edition = getattr(reference, 'edition', None)
        entry.month = getattr(reference, 'month', None)
        entry.note = getattr(reference, 'note', None)
        entry.journaltitle = getattr(reference, 'journal', None)
        entry.pages = getattr(reference, 'pages', None)
        titles = getattr(reference, 'booktitle', ())
        if len(titles) >= 1:
            entry.booktitle = titles[0]
        if len(titles) > 1:
            entry.booksubtitle = titles[1]
            if len(titles) > 2:
                entry.booksubtitle += u". " + titles[2]
        entry.type = getattr(reference, 'type', None)
        entry.chapter = getattr(reference, 'chapter', None)
        if getattr(reference, 'language', None) == 'de':
            entry.hyphenation = 'ngerman'
        else:
            entry.hyphenation = 'english'
        title = getattr(reference.uniform_title, 'uniform_title', ())
        origtitle = u""
        if title:
            for t in title:
                origtitle += t + u". "
            entry.origtitle = origtitle[:-2]
        year = getattr(reference.uniform_title, 'year', None)
        if year:
            origdate = year
        else:
            origdate = unicode(getattr(reference.uniform_title, 'post', u"")) + u"/" + unicode(getattr(reference.uniform_title, 'ante', u""))
        try:
            entry.origdate = origdate
        except Exception:
            pass
            
            
        if IBook.providedBy(reference):
            entry.entry_type = 'Book'
        if IIncollection.providedBy(reference):
            entry.entry_type = 'InCollection'
        if IArticle.providedBy(reference):
            entry.entry_type = 'Article'

        name = namechooser.chooseName(None, entry)
        bibliography[name] = entry

        map[reference.__name__] = entry.__name__

        dcdata = IAnnotations(reference).get(DCkey)
        annotations = IAnnotations(entry)
        annotations[DCkey] = dcdata

        grantCreator(entry)

        if 1 == 0: #hack for testing
            break 


    for example in findObjectsProviding(site, IExample):
        
        grantCreator(example)
        
        if '.plaintext' in example.source_type:
            example.source_type = 'plaintext'
        if '.rest' in example.source_type:
            example.source_type = 'rest'
            
        example.reference = bibliography[map[example.reference.__name__]]


    for comment in findObjectsProviding(site, IComment):
        
        grantCreator(comment)
        
        if '.plaintext' in comment.source_type:
            comment.source_type = 'plaintext'
        if '.rest' in comment.source_type:
            comment.source_type = 'rest'
            
    if 1 == 0:
        raise Exception
    
