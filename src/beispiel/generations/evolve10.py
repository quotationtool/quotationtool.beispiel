def evolve(context):
    """ After evolution from 2009 version to 2011 version:

    - replace old signup principal folder with new one

    """

    # We moved the imports here because of getInfo which only takes
    # the __doc__ string in evolve. getInfo should not import
    # anything.
    import zope.interface
    import zope.component
    from zope.app.zopeappgenerations import getRootFolder
    from zope.app.generations.utility import findObjectsProviding
    from zope.app.component import hooks
    from zope.intid.interfaces import IIntIds

    from quotationtool.site.interfaces import IQuotationtoolSite
    from quotationtool.user.signup import SignupPrincipalFolder
    from zope.app.authentication.principalfolder import IInternalPrincipal


    root = getRootFolder(context)

    site = None
    for s in findObjectsProviding(root, IQuotationtoolSite):
        site = s
        break
    if site is None:
        raise Exception('No quotationtool site!')
    hooks.setSite(site)

    sm = site.getSiteManager()

    intids = zope.component.getUtility(IIntIds, context = site)

    pau = sm['default']['pau']

    old_folder = pau['signup_principal_folder']
    intids.register(old_folder)

    new_folder = pau['SignupPrincipalFolder'] = SignupPrincipalFolder()
    pau.authenticatorPlugins = [new_folder.__name__]
    new_folder.prefix = "users."
    new_folder.signup_roles = [u'quotationtool.Member']

    if 1 == 0:
        raise Exception("%d principals" % len(old_folder.values()))

    still_in_old_folder = True
    while still_in_old_folder:
        name = old_folder.keys()[0]
        new_folder[name] = old_folder[name]
        assert(new_folder[name]._password == old_folder[name]._password)
        assert(new_folder[name]._passwordManagerName == old_folder[name]._passwordManagerName)
        del old_folder[name]
        if len(old_folder.values()) == 0:
            still_in_old_folder = False
    
    del pau['signup_principal_folder']

    if 1 == 0:
        raise Exception
        



        

