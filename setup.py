from setuptools import setup, find_packages

setup(
    name='Vault',
    version='0.1.0',
    author='Colin Davis',
    author_email='colinmichaelsdavis@gmail.com',
    packages=find_packages(),
    url='https://github.com/colin-m-davis/kvs',
    license='LICENSE.txt',
    description='Key-value store in Python',
    long_description=open('README.md').read(),
    install_requires=[
        'pylint',
    ],
    entry_points = {
        'console_scripts': [
            'vault = vault.__main__:main'
        ]
    }
)