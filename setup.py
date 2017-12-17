from setuptools import setup, find_packages

setup(
    name="xoxzo_cloudpy",
    version="0.4.0",
    author="Xoxzo Inc.",
    author_email="help@xoxzo.com",
    description=("Xoxzo Public API library"),
    license="MIT",
    keywords="xoxzo telephony api",
    url="https://github.com/xoxzo/xoxzo.cloudpy",
    packages=find_packages('.'),
    namespace_packages=['xoxzo'],
    install_requires=[
        'requests >=2.9.1',
    ],
    test_suite='tests'
)

