__author__ = 'bagrat'

from setuptools import setup, find_packages

version = '0.1'

tests_require = ['nose', 'coverage']

install_requires = []

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
    'description': 'Easy package versioning and release management',
    'author': 'Bagrat Aznauryan',
    'url': 'git@github.com:n9code/pylease.git',
    'download_url': 'git@github.com:n9code/pylease.git',
    'author_email': 'bagrat@aznauryan.org',
    'version': version,
    'install_requires': install_requires,
    'tests_require': tests_require,
    'classifiers': classifiers,
    'packages': find_packages(),
    'name': 'pylease',
    'license': 'MIT',
    'keywords': 'release version versioning',
    'entry_points': {
        'console_scripts': [
            'pylease = pylease.main:main'
        ]
    }
}

setup(**config)
