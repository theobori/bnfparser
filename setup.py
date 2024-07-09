"""setup module"""

from setuptools import setup, find_packages

with open('README.md', encoding="utf-8") as f:
    readme = f.read()

with open('LICENSE', encoding="utf-8") as f:
    _license = f.read()

with open('requirements.txt', encoding="utf-8") as f:
    required = f.read().splitlines()

setup(
    name='bnfparser',
    version='0.1.0',
    install_requires=required,
    description='BNF parser',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Théo Bori',
    author_email='nagi@tilde.team',
    url='https://github.com/theobori/bnf-parser',
    license=_license,
    packages=find_packages(),
    include_package_data=True,
    test_suite="tests",
)
