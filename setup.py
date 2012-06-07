import os
from setuptools import setup, find_packages

readme = open(os.path.join(os.path.dirname(__file__), 'README'))
README = readme.read()
readme.close()

version = "0.1"


setup(name='python-odesk3',
      version=version,
      description='Python3 bindings to oDesk API',
      long_description=README,
      author='oDesk',
      author_email='python@odesk.com',
      maintainer='Volodymyr Hotsyk',
      maintainer_email='gotsyk@gmail.com',
      install_requires=['oauth2',],
      dependency_links = ['https://github.com/hades/python-oauth2/tarball/python3#egg=oauth2',],
      packages=find_packages(),
      license = 'BSD',
      download_url ='http://github.com/odesk/python-odesk',
      url='http://odesk.github.com/python-odesk',
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Web Environment',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   'Topic :: Utilities',],)
