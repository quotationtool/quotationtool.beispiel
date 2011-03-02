def evolve(context):
    """ Evolution for new feature: tagging examples, html source type
    for examples and comments

    - set the examples' source_type attribute to
      'html'

    - cook an html source from examples quotation and store it on the
      quotation attribute.

    - Do the same thing for comments  

    """
    import zope.interface
    import zope.component
    from zope.app.zopeappgenerations import getRootFolder
    from zope.app.generations.utility import findObjectsProviding
    from zope.app.component import hooks
    from zope.intid.interfaces import IIntIds

    from quotationtool.site.interfaces import IQuotationtoolSite 
    from quotationtool.figuresng.iexample import IExample
    from quotationtool.renderer.interfaces import IHTMLRenderer
    from quotationtool.commentary.interfaces import IComment

    root = getRootFolder(context)

    site = None
    for s in findObjectsProviding(root, IQuotationtoolSite):
        site = s
        break


    def cookHTMLSource(obj, source = 'quotation', source_type = 'source_type'):
        if getattr(obj, source_type) == 'html':
            return getattr(ob, source)

        _source = zope.component.createObject(
            getattr(obj, source_type),
            getattr(obj, source))
        renderer = IHTMLRenderer(_source)
        
        if getattr(obj, source_type) == 'rest':
            return renderer.render()

        if getattr(obj, source_type) == 'plaintext':
            rc = u"<p>"
            rc += renderer.render().strip()
            rc += u"</p>"
            rc = rc.replace('<br />', '</p>\n<p>')
            rc = rc.replace('<br/>', '</p>\n<p>')
            return rc

    i = 0
    for example in findObjectsProviding(site, IExample):
        example.quotation = cookHTMLSource(example, source = 'quotation')
        example.source_type = 'html'
        i += 1

    for comment in findObjectsProviding(site, IComment):
        comment.comment = cookHTMLSource(comment, source = 'comment')
        comment.source_type = 'html'

    if 1 == 2:
        raise Exception(i)
