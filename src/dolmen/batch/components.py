# -*- coding: utf-8 -*-

import sys
from os import path
from urllib.parse import urlencode

from cromlech.browser import IRenderable
from cromlech.i18n import getLocalizer
from cromlech.location import get_absolute_url
from dolmen.template import TALTemplate
from z3c.batching.batch import Batch
from zope.interface import implementer


TEMPLATES_DIR = path.join(path.dirname(__file__), 'templates')


if sys.version_info >= (3,):
    unicode = str


def safe_str(v):
    if isinstance(v, bytes):
        return v
    elif isinstance(v, unicode):
        return v.encode('utf-8')
    else:
        raise TypeError("Can't encode param %s" % v)


def template_path(filename):
    return path.join(TEMPLATES_DIR, filename)


def flatten_params(params):
    for k, v in params.items():
        if isinstance(v, (bytes, unicode)):
           yield k, v
        else:
            try:
                iterator = iter(v)
                for i in iterator:
                    yield k, i
            except TypeError:
                yield k, str(v)


@implementer(IRenderable)
class Batcher(object):

    template = TALTemplate(template_path('batch.pt'))

    def __init__(self, context, request, prefix='batch', size=10):
        self.context = context
        self.request = request
        self.url = get_absolute_url(self.context, self.request)
        self.prefix = prefix
        self.size = size
        self.batch = None

    @property
    def available(self):
        return bool(self.batch is not None and len(self.batch.batches))

    def previous(self):
        batch = self.batch.batches[0]
        while batch is not self.batch:
            yield batch
            batch = batch.next

    def next(self):
        batch = self.batch.next
        while batch:
            yield batch
            batch = batch.next

    def batch_info(self, start=0):
        start = int(self.request.form.get(self.prefix + '.start', start))
        size = int(self.request.form.get(self.prefix + '.size', self.size))
        return start, size

    def update(self, sequence, *args, **kw):
        start, size = self.batch_info()
        self.batch = Batch(sequence, start=start, size=size)

    def batch_url(self, batch):
        start_param = self.prefix + ".start"
        size_param = self.prefix + ".size"
        params = [(k, safe_str(v))
                  for k, v in flatten_params(self.request.form)
                  if k not in (start_param, size_param)]
        params.append((start_param, batch.start))
        params.append((size_param, batch.size))
        return self.url + '?' + urlencode(params)

    def namespace(self):
        namespace = {}
        namespace['batch'] = self.batch
        namespace['batcher'] = self
        namespace['context'] = self.context
        return namespace

    @property
    def translate(self):
        """Returns the current localizer using the thread cache.
        Please note that the cache might be 'None' if nothing was set up.
        None will, most of the time, mean 'no translation'.
        """
        localizer = getLocalizer()
        if localizer is not None:
            localizer.translate
        return None
 
    def render(self, *args, **kwargs):
        if not self.available:
            return u''
        return self.template.render(
            self, translate=self.translate, **self.namespace())
