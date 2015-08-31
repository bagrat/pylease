from functools import partial
from setuptools import setup, find_packages
import pylease
import os

download_url = "https://github.com/n9code/pylease/archive/v{version}.tar.gz".format(version=pylease.__version__)

here = os.path.abspath(os.path.dirname(__file__))
print(here)
here_path = partial(os.path.join, here)
deps_test_path = here_path('deps/test.txt')
deps_core_path = here_path('deps/core.txt')
readme_path = here_path('README.rst')

print(deps_core_path)

with open(deps_test_path) as req:
    tests_require = req.read().split('\n')

with open(deps_core_path) as req:
    install_requires = req.read().split('\n')

with open(readme_path) as desc:
    long_desc = desc.read()

classifiers = ['License :: OSI Approved :: MIT License',
               'Intended Audience :: Developers',
               'Natural Language :: English',
               'Programming Language :: Python',
               'Programming Language :: Python :: 2',
               'Programming Language :: Python :: 3',
               'Operating System :: POSIX',
               'Operating System :: POSIX :: Linux',
               'Operating System :: MacOS',
               'Topic :: Software Development :: Libraries :: Python Modules']

config = {
    'name': 'pylease',
    'description': 'Easy package versioning and release management',
    'long_description': long_desc,
    'author': 'Bagrat Aznauryan',
    'url': 'git@github.com:n9code/pylease.git',
    'download_url': download_url,
    'author_email': 'bagrat@aznauryan.org',
    'version': pylease.__version__,
    'install_requires': install_requires,
    'tests_require': tests_require,
    'classifiers': classifiers,
    'packages': find_packages(),
    'license': 'MIT',
    'keywords': 'release version versioning',
    'entry_points': {
        'console_scripts': [
            'pylease = pylease.main:main'
        ]
    }
}

setup(**config)
