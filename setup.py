import os
from setuptools import setup

from ec2audit import __version__

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='ec2audit',
      version=__version__,
      description='Dump all EC2 information to a folder suitable for version control',
      long_description=read('README.rst'),
      url='http://github.com/SimpleFinance/ec2audit',
      author='Cosmin Stejerean',
      author_email='cosmin@offbytwo.com',
      license='Apache License 2.0',
      packages=['ec2audit'],
      scripts=['bin/ec2audit'],
      tests_require=open('test-requirements.txt').readlines(),
      install_requires=open('requirements.txt').readlines(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Utilities'
        ]
     )
