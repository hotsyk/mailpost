from distutils.core import setup
import os

from mailpost import get_version

setup(name='mailpost',
      version=get_version().replace(' ', '-'),
      description='',
      long_description='',
      author='',
      author_email='',
      url='',
      download_url='',
      package_dir={'mailpost': 'mailpost'},
      packages=[''],
      package_data={'mailpost': ''},
      classifiers=['Development Status :: 1 - Alpha',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   'Topic :: Communications :: Email',
                   'Topic :: Utilities'],)