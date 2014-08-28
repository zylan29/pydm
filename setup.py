from setuptools import setup, find_packages

NAME = "pydm"
DESCRIPTION = "python binding for linux device mapper"
AUTHOR = "Ziyang Li"
AUTHOR_EMAIL = "anzigly@gmail.com"
URL = "https://github.com/anzigly/pydm"
setup(
    name=NAME,
    version="0.3.3",
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="Apache V2",
    url=URL,
    packages=find_packages(),
    keywords='python device mapper'
)
