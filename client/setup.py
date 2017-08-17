from setuptools import setup, find_packages
import sys, os

version = '1.0'

setup(name='py-oas-client',
      version=version,
      description='Python Online Accounting System (client)',
      long_description="""\
Python Online Accounting System (client)
""",
      classifiers=['Development Status :: 2 - Pre-Alpha',
                   'Environment :: Console',
                   'Intended Audience :: Financial and Insurance Industry',
                   'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
                   'Programming Language :: Python',
                   'Topic :: Office/Business :: Financial :: Accounting'
                   ],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='Accounting',
      author='Christophe Alexandre',
      author_email='ch dot alexandre at bluewin dot ch',
      url='http://code.google.com/p/py-oas-client',
      license='LGPL',
      packages=find_packages(exclude=['ez_setup', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
          'mechanize',
          'httplib2',
      ],
      setup_requires=[
          'nose>=1.0',
      ],
      dependency_links=[
          # web access to package repository
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      test_suite='nose.collector',
      tests_require='nose',
      )
