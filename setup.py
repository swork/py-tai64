import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "tai64",
    version = "1.0.0",
    url = 'http://bitbucket.com/hinnerk/TAI64Converter',
    license = 'BSD',
    description = "Converts TAI64(n) string to datetime.datetime (UTC) object.",
    long_description = read('README.rst'),

    author = 'Hinnerk Haardt',
    author_email = 'hinnerk@randnotizen.de',

    packages = find_packages('tai64'),
    package_dir = {'': 'tai64'},
    
    install_requires = ['setuptools'],

    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Other/Nonlisted Topic',
    ]
)