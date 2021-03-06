# -*- coding: utf-8 -*-
import codecs
import os
import re
import setuptools
from distutils.util import convert_path


main_ns = {}
ver_path = convert_path('mediawikiapi/version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)


def local_file(file):
  return codecs.open(
    os.path.join(os.path.dirname(__file__), file), 'r', 'utf-8'
  )


install_reqs = [
  line.strip()
  for line in local_file('requirements.txt').readlines()
  if line.strip() != ''
]

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = local_file('README.md').read()

setuptools.setup(
  name = "mediawikiapi",
  version = main_ns['__version__'],
  author = "Taras Lehinevych",
  author_email = "mediawikiapi@taraslehinevych.me",
  description = "Wikipedia API on Python",
  license = "MIT",
  keywords = "python wikipedia API mediawiki",
  url = "https://github.com/lehinevych/MediaWikiAPI",
  install_requires = install_reqs,
  packages = ['mediawikiapi'],
  long_description = long_description,
  classifiers = [
    'Development Status :: 4 - Beta',
    'Topic :: Software Development :: Libraries',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ]
)
