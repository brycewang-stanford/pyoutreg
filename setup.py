"""
Setup script for pyoutreg package.
A Python implementation of Stata's outreg2 command for exporting regression results.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pyoutreg",
    version="0.1.0",
    author="Bryce Wang",
    author_email="brycewang@example.com",
    description="A Python implementation of Stata's outreg2 for exporting regression results",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/brycewang/pyoutreg",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Scientific/Engineering",
        "Topic :: Office/Business :: Office Suites",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pandas>=1.3.0",
        "numpy>=1.20.0",
        "statsmodels>=0.12.0",
        "linearmodels>=4.25",
        "openpyxl>=3.0.0",
        "python-docx>=0.8.11",
        "scipy>=1.7.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
