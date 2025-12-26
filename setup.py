"""Setup script for sqlean-stubs."""

from setuptools import find_packages, setup

setup(
    name="sqlean-stubs",
    version="0.0.3",
    packages=find_packages(),
    package_data={
        "sqlean": ["py.typed"],
    },
    python_requires=">=3.8",
    description="Type hints for sqlean.py (sqlite3 + extensions)",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/nalgeon/sqlean.py",
    author="Type Hints Contributors",
    license="zlib/libpng",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Typing :: Typed",
    ],
)
