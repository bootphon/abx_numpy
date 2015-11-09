'''
abx_numpy: Small ABX evaluation

Note that "python setup.py test" invokes pytest on the package. With appropriately
configured setup.cfg, this will check both xxx_test modules and docstrings.

Copyright 2015, Roland Thiolliere.
Licensed under GPLv3.
'''
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

# This is a plug-in for setuptools that will invoke py.test
# when you run python setup.py test
class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest  # import here, because outside the required eggs aren't loaded yet
        sys.exit(pytest.main(self.test_args))


version = "0.2.1"

setup(name="abx_numpy",
      version=version,
      description="Small ABX evaluation",
      long_description=open("README.rst").read(),
      classifiers=[ # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 1 - Planning',
        'Programming Language :: Python'
      ],
      keywords="ABX numpy features evaluation", # Separate with spaces
      author="Roland Thiolliere",
      author_email="rolthiolliere@gmail.com",
      url="",
      license="GPLv3",
      packages=find_packages(exclude=['examples', 'tests']),
      include_package_data=True,
      modules=['abx_numpy'],
      zip_safe=False,
      tests_require=['pytest'],
      cmdclass={'test': PyTest},

      # TODO: List of packages that this one depends upon:
      install_requires=['numpy', 'scipy'],
      # TODO: List executable scripts, provided by the package (this is just an example)
      # entry_points={
      #   'console_scripts':
      #       ['abx_numpy=abx_numpy:main']
      # }
)
