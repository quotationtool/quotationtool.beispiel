"""Manage zodb schemas of the 'Archiv des Beispiels' project.

generation 1: evolve from 2006 version (requires code of the 2006
version in the python path.

generation 2: change family of various catalog extents from
BTrees.family64 to default (BTrees.family32).

generation 3: switched to figuresng (figures next generation),
resturcturing of relation catalog, added commentaboutreference
"""

from zope.app.generations.generations import SchemaManager

BeispielSchemaManager = SchemaManager(
    minimum_generation = 5,
    generation = 10,
    package_name = 'beispiel.generations',
    )
