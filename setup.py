# -*- coding: utf-8 -*-
"""Setup for beispiel application

$Id$
"""
from setuptools import setup, find_packages
import os

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

name='beispiel'

setup(
    name = name,
    version='0.1.0',
    description="Beispiel quotationtool application",
    long_description=(
        read('README')
        + '\n' +
        'Detailed Documentation\n'
        '**********************\n'
        + '\n' +
        read('src', 'beispiel', 'README.txt')
        + '\n' +
        'Download\n'
        '********\n'
        ),
    keywords='Archiv des Beispiels',
    author=u"Christian Lueck",
    author_email='cluecksbox@googlemail.com',
    url='',
    license='ZPL 2.1',
    # Get more from http://www.python.org/pypi?%3Aaction=list_classifiers
    classifiers=['Programming Language :: Python',
                 'Environment :: Web Environment',
                 'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
                 'Framework :: BlueBream',
                 ],
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires = [
        'setuptools',
        'ZODB3',
        'zope.interface',
        'zope.schema',
        'zope.component',
        'zope.i18nmessageid',

        # for bb instance:
        'zope.securitypolicy',
        'zope.annotation',
        'zope.browserresource',
        'zope.app.dependable',
        'zope.app.appsetup',
        'zope.app.content',
        'zope.publisher',
        'zope.app.broken',
        'zope.app.component',
        'zope.app.generations',
        'zope.app.error',
        'zope.app.interface',
        'zope.app.publisher',
        'zope.app.security',
        'zope.app.form',
        'zope.app.i18n',
        'zope.app.locales',
        'zope.app.zopeappgenerations',
        'zope.app.principalannotation',
        'zope.app.basicskin',
        'zope.app.rotterdam',
        'zope.app.folder',
        'zope.app.wsgi',
        'zope.formlib',
        'zope.i18n',
        'zope.app.pagetemplate',
        'zope.app.schema',
        'zope.app.container',
        'zope.app.debug',
        'z3c.testsetup',
        'zope.app.testing',
        'zope.testbrowser',
        'zope.login',
        'zope.app.zcmlfiles',

        # quotationtool:
        'quotationtool.site',
        'quotationtool.security',
        'quotationtool.renderer',
        'quotationtool.relation',
        'quotationtool.skin',
        'quotationtool.search',
        'quotationtool.bibliography',
        'quotationtool.biblatex',
        'quotationtool.figuresng',
        'quotationtool.commentary',
        'quotationtool.categorization',
        'quotationtool.user',
        'quotationtool.locales',
        
        #BBB: remove in 0.2.0
        'quotationtool.referatory',
        'quotationtool',
        
        # for old DB items
        'zope.app.folder',
        'zope.app.session',
        'zope.app.error',
        'zope.app.intid',
        'zope.app.securitypolicy',

        # ice.control:
        'ice.control',
        
        'z3c.template',
        'z3c.macro',
        'z3c.pagelet',
        'z3c.layer.pagelet',
        'zope.app.publication',
        'zope.browserpage',
        'zope.publisher',
        'z3c.formui',
        'z3c.form',
        'zc.resourcelibrary',
        'z3c.menu.ready2go',

        'zope.app.pagetemplate',
        'zope.viewlet',
        'zope.app.component',
        ],
    extras_require = dict(
        test = [
            'zope.testing',
            'zope.configuration',
            ],
        ),
    entry_points = """
    [paste.app_factory]
    main = beispiel.startup:application_factory

    [paste.global_paster_command]
    shell = beispiel.debug:Shell
    """,

    )
