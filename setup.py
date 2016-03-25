from setuptools import setup, find_packages

setup(
    name="xoxzo.cloudpy",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    test_suite = 'tests'
)
