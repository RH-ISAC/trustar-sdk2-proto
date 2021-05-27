from setuptools import setup, find_packages
from glob import glob

# read version
version_globals = {}
with open("trustar2/version.py") as fp:
    exec(fp.read(), version_globals)
version = version_globals['__version__']

setup(
    name='trustar2',
    packages=find_packages(exclude=("tests",)),
    version=version,
    author='TruSTAR Technology, Inc.',
    author_email='support@trustar.co',
    url='https://github.com/trustar/trustar-sdk2-proto/',
    download_url='https://github.com/trustar/trustar-sdk2-proto/tarball/%s' % version,
    description='Python SDK2 for the TruSTAR REST API',
    license='MIT',
    install_requires=['json_log_formatter',
                      'future',
                      'python-dateutil',
                      'pytz',
                      'requests',
                      'configparser',
                      'dateparser',
                      'unicodecsv',
                      'tzlocal',
                      'PyYAML',
                      'six'
                      ],
    include_package_data=True,
    use_2to3=True
)
