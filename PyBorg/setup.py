#!/usr/bin/env python

from setuptools import setup

setup(name='PyBorg',
      version='0.1',
      description='Borg MOEA in Python',
      author='David Hadka',
      author_email='dhadka@users.noreply.github.com',
      license="GNU GPL version 3",
      url='https://github.com/Project-Platypus/PyBorg',
      packages=['pyborg'],
      install_requires=['platypus'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Education',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Topic :: Scientific/Engineering :: Artificial Intelligence',
          'Topic :: Scientific/Engineering :: Mathematics',
          'Topic :: Software Development :: Libraries :: Python Modules',
          ],
     )