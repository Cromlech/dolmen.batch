# -*- coding: utf-8 -*-

from cromlech.browser.testing import XMLDiff, TestResponse, TestRequest
from cromlech.browser import IPublicationRoot
from dolmen.batch import Batcher
from zope.interface import implements
from zope.location import Location


NO_BATCH = '''
<div class="batch">
  <ul>
    <li class="current">1</li>
  </ul>
</div>
'''

BATCHED = '''
<div class="batch">
  <ul>
    <li class="current">1</li>
    <li class="next">
      <a href="http://localhost?batch.start=2&amp;batch.size=2">2</a>
    </li>
    <li class="next">
      <a href="http://localhost?batch.start=4&amp;batch.size=2">3</a>
    </li>
    <li class="next">
      <a href="http://localhost?batch.start=6&amp;batch.size=2">4</a>
    </li>
  </ul>
</div>
'''

BATCHED_ADV = '''
<div class="batch">
  <ul>
    <li class="previous">
      <a href="http://localhost?batch.start=0&amp;batch.size=2">1</a>
    </li>
    <li class="previous">
      <a href="http://localhost?batch.start=2&amp;batch.size=2">2</a>
    </li>
    <li class="current">3</li>
    <li class="next">
      <a href="http://localhost?batch.start=6&amp;batch.size=2">4</a>
    </li>
  </ul>
</div>
'''


def test_batch():

    sequence = [1, 3, 5, 7, 9, 11, 13, 15]

    class Publishable(Location):
        implements(IPublicationRoot)

    root = Publishable()
    request = TestRequest()
    batcher = Batcher(root, request)
    batcher.update(sequence)
    assert not XMLDiff(batcher.render(), NO_BATCH)

    request = TestRequest(form={'batch.size': 2})
    batcher = Batcher(root, request)
    batcher.update(sequence)
    assert not XMLDiff(batcher.render(), BATCHED)

    request = TestRequest(form={'batch.size': 2, 'batch.start': 4})
    batcher = Batcher(root, request)
    batcher.update(sequence)
    assert not XMLDiff(batcher.render(), BATCHED_ADV)


def test_batch_unicode_param():

    sequence = range(10)
    
    class Publishable(Location):
        implements(IPublicationRoot)

    root = Publishable()
    request = TestRequest(
                form={'batch.size': 2, 'batch.start': 4, 'x':u'héhô'})
    batcher = Batcher(root, request)
    batcher.update(sequence)
    content = batcher.render()  # must not raise
    # assert page param is url encoded
    assert 'http://localhost?x=h%C3%A9h%C3%B4' in content


def test_batch_multi_param():

    sequence = range(10)
    
    class Publishable(Location):
        implements(IPublicationRoot)

    root = Publishable()
    request = TestRequest(
                form={'batch.size': 2, 'batch.start': 4, 'x':[u'a', u'b']})
    batcher = Batcher(root, request)
    batcher.update(sequence)
    assert ('http://localhost?x=a&amp;x=b&amp;batch.start=0&amp;batch.size=2'
            in batcher.render())
    
