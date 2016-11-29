# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os.path import join

name = 'dolmen.batch'
version = '0.2'
readme = open(join('src', 'dolmen', 'batch', 'README.txt')).read()
history = open(join('docs', 'HISTORY.txt')).read()

install_requires = [
    'cromlech.browser >= 0.5',
    'cromlech.i18n',
    'dolmen.location >= 0.2',
    'dolmen.template >= 0.2',
    'setuptools',
    'z3c.batching',
    'zope.interface',
    ]

tests_require = [
    'cromlech.browser [test]',
    'grokcore.component [test]',
    'zope.location',
    ]

setup(name=name,
      version=version,
      description='Dolmen batch handler',
      long_description=readme + '\n\n' + history,
      keywords='Cromlech Dolmen Batch',
      author='The Dolmen team',
      author_email='dolmen@list.dolmen-project.org',
      url='http://gitweb.dolmen-project.org/',
      download_url='',
      license='ZPL',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'': 'src'},
      namespace_packages=['dolmen'],
      include_package_data=True,
      platforms='Any',
      zip_safe=False,
      tests_require=tests_require,
      install_requires=install_requires,
      extras_require={'test': tests_require},
      classifiers=[
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
      ],
)
