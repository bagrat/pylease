import pylease

__author__ = 'bagrat'

from setuptools import setup, find_packages

download_url = "https://github.com/n9code/pylease/archive/v{version}.tar.gz".format(version=pylease.__version__)

with open('./deps/test.txt') as req:
    tests_require = req.read().split('\n')

with open('./deps/core.txt') as req:
    install_requires = req.read().split('\n')

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
