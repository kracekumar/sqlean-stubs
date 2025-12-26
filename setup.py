"""Setup script for sqlean-stubs."""

from setuptools import setup, find_packages

setup(
    name="sqlean-stubs",
    version="3.50.4",
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
    license="Zlib",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Zlib License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Typing :: Typed",
    ],
)
