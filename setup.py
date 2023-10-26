import setuptools

__name__ = "base-descriptor"
__version__ = "1.2"
__author__ = "Tyler Bruno"
__description__ = (
    "A simple, fast, typed, and tested abstract and base classes for a "
    "python3.6+ Non Data Descriptor, Data Descriptor, and Slottable Data "
    "Descriptor.")
__keywords__ = ("descriptor data-descriptor non-data-descriptor "
                "slottable-data-descriptor")
__url__ = "https://github.com/tybruno/base-descriptor"
__license__ = "MIT"
__packages__ = setuptools.find_packages()
__install_requires__ = []
__classifiers__ = [
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3 :: Only",
    "Topic :: Software Development :: Libraries :: Python Modules",
]

with open("README.md", "r", encoding="utf-8") as file:
    README = file.read()

setuptools.setup(
    name=__name__,
    version=__version__,
    author=__author__,
    description=__description__,
    long_description=README,
    long_description_content_type="text/markdown",
    keywords=__keywords__,
    url=__url__,
    license=__license__,
    packages=__packages__,
    install_requires=__install_requires__,
    classifiers=__classifiers__,
    python_requires=">=3.6",
)
