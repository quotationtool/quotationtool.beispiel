import random
import datetime

import zope.interface
import zope.component
from zope.intid.interfaces import IIntIds
from zope.component import hooks

from quotationtool.figuresng.iexample import IExampleContainer
import interfaces


class ExampleOfDay(object):
    """A local utility that returns a randomly picked example of the
    day."""

    zope.interface.implements(interfaces.IRandomExample)

    last_visited = None
    example = None

    def getExample(self):
        intids = zope.component.getUtility(IIntIds, context = hooks.getSite())
        today = str(datetime.date.today())
        if self.last_visited == today and self.example:
            example = intids.queryObject(self.example, default = None)
            if example:
                # maybe it was deleted!
                return example
        # pick a new one
        self.last_visited = today
        example_container = zope.component.getUtility(
            IExampleContainer, context = hooks.getSite())
        count = IExampleContainer(example_container)._count
        if count == 0:
            return None
        tried = 0 # do not try to find an example endlessy. There
                  # might be no examples in the container while
                  # count is arbitrary.
        example = None
        while self.example is None and tried < 10:
            i = random.randint(0, count)
            example = example_container.get(unicode(i), None)
            tried += 1
            #raise Exception(i, example)
        if example is not None:
            self.example = intids.getId(example)
            return example
        else:
            return None
