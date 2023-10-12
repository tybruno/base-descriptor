import setuptools

__version__ = "0.1"
__author__ = "Tyler Bruno"
INSTALL_REQUIRES = []

with open("README.md", "r", encoding="utf-8") as file:
    README = file.read()

setuptools.setup(
    name="abstract-descriptor",
    version=__version__,
    author=__author__,
    long_description=README,
    long_description_content_type="text/markdown",
    keywords="descriptor data-descriptor non-data-descriptor "
             "slottable-data-descriptor",
    url="https://github.com/tybruno/abstract-descriptor",
    license="MIT",
    packages=setuptools.find_packages(),
    install_requires=INSTALL_REQUIRES,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.6",
)
