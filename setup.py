from setuptools import setup, find_packages

setup(
    name="xoxzo.cloudpy",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'requests >=2.9.1',
    ],
    test_suite = 'tests'
)
