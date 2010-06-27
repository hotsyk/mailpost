from distutils.core import setup

version = __import__('mailpost').get_version()


setup(name='mailpost',
      version=version,
      description='A package that maps incoming email to HTTP requests',
      long_description='A package that maps incoming email to HTTP requests',
      author='oDesk, www.odesk.com',
      author_email='developers@odesk.com',
      packages = ['mailpost', 'mailpost.management', 
                  'mailpost.management.commands'],
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