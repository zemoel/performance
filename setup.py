#!/usr/bin/env python3

# Update dependencies:
#
#  - python2 -m performance venv create
#  - venv/cpython2<tab>/bin/python -m pip list --outdated
#  - update performance/requirements.txt
#  - increase performance major version of a benchmark dependency is upgraded
#  - (see also pip-tools and pipdeptree tools)
#
# Prepare a release:
#
#  - git pull --rebase
#  - run tests: tox
#  - maybe update version in setup.py and performance/__init__.py
#  - set release date in changelog (README.rst)
#  - git commit -a -m "prepare release x.y"
#  - git push
#
# Release a new version:
#
#  - git tag VERSION
#  - git push --tags
#  - python3 setup.py register sdist bdist_wheel upload
#    (need wheel: sudo python3 -m pip install -U setuptools wheel)
#
# After the release:
#
#  - set version to n+1
#  - git commit -a -m "post-release"
#  - git push

VERSION = '0.3.1'

DESCRIPTION = 'Python benchmark suite'
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python',
]


# put most of the code inside main() to be able to import setup.py in
# unit tests
def main():
    import io
    from setuptools import setup

    with io.open('README.rst', encoding="utf8") as fp:
        long_description = fp.read().strip()

    packages = [
        'performance',
        'performance.benchmarks',
        'performance.benchmarks.data',
        'performance.benchmarks.data.2to3',
        'performance.benchmarks.pybench',
        'performance.benchmarks.pybench.package',
        'performance.tests',
        'performance.tests.data',
    ]
    data_files = [
        'spambayes_hammie.pkl',
        'spambayes_mailbox',
        'telco-bench.b',
        'w3_tr_html5.html',
    ]
    data = {
        'performance': ['requirements.txt'],
        'performance.benchmarks.data': data_files,
        'performance.benchmarks.data.2to3': ['README', '*.txt'],
        'performance.benchmarks.pybench': ['LICENSE', 'README'],
        'performance.tests.data': ['*.json'],
    }

    options = {
        'name': 'performance',
        'version': VERSION,
        'author': 'Collin Winter and Jeffrey Yasskin',
        'license': 'MIT license',
        'description': DESCRIPTION,
        'long_description': long_description,
        'url': 'https://github.com/python/benchmarks',
        'classifiers': CLASSIFIERS,
        'packages': packages,
        'package_data': data,
        'install_requires': ["virtualenv"],
        'entry_points': {
            'console_scripts': ['pyperformance=performance.cli:main']
        }
        # Note: the performance package has no direct external dependencies:
        # it installs dependencies itself by creating virtual environments
    }
    setup(**options)

if __name__ == '__main__':
    main()
