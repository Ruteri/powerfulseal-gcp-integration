import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='powerfulseal',
    version='2.2.0',
    author='Mikolaj Pawlikowski',
    author_email='mikolaj@pawlikowski.pl',
    url='https://github.com/bloomberg/powerfulseal',
    packages=find_packages(),
    license=read('LICENSE'),
    description='PowerfulSeal - a powerful testing tool for Kubernetes clusters',
    long_description=read('README.md'),
    install_requires=[
        'ConfigArgParse>=0.11.0,<1',
        'Flask>=1.0.0,<2',
        'termcolor>=1.1.0,<2',
        'openstacksdk>=0.10.0,<1',
        'spur>=0.3.20,<1',
        'kubernetes>=8.0.1<9',
        'PyYAML>=3.12,<4',
        'jsonschema>=2.6.0,<3',
        'boto3>=1.5.15,<2.0.0',
        'google-api-python-client>=1.7.9',
        'azure>=4.0.0,<5.0.0',
        'future>=0.16.0,<1',
        'requests>=2.21.0,<3',
        'prometheus_client>=0.3.0,<0.4.0',
        'flask-cors>=3.0.6,<4',
        'flask-swagger-ui>=3.18.0<4',
        'coloredlogs>=10.0.0,<11.0.0',
        'six>=1.12.0,<2',
        'paramiko>=2.5.0,<3'
    ],
    extras_require={
        'testing': [
            'pytest>=3.0,<4',
            'pytest-cov>=2.5,<3',
            'mock>=2,<3',
        ]
    },
    entry_points={
        'console_scripts': [
            'seal = powerfulseal.cli.__main__:start',
            'powerfulseal = powerfulseal.cli.__main__:start',
        ]
    },
    classifiers=[
	    'Development Status :: 4 - Beta',
	    'Intended Audience :: Developers',
	    'Topic :: Software Development :: Test Tools',
	    'Programming Language :: Python :: 3',
    ],
    python_requires='>=3',
    include_package_data=True,
)
