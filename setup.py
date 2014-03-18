from setuptools import setup, find_packages
NAME="pydm"
DESCRIPTION="python binding for linux device mapper"
AUTHOR="Ziyang Li"
AUTHOR_EMAIL="lzynudt@gmail.com"
URL="https://github.com/anzigly/pydm"
setup(
    name=NAME,
    version="0.2.0",
    description=DESCRIPTION,
    long_description=open("README.md").read(),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="Apache V2",
    url=URL,
    packages=find_packages(),
    keywords='device mapper'
)
