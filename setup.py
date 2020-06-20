from pathlib import Path

from setuptools import setup, find_packages


def get_version():
    version = {}
    with open("./click_constrained_option/_version.py") as f:
        exec(f.read(), version)
    return version["__version__"]


def get_readme():
    return (Path(__file__).parent / "README.md").read_text()


setup(
    name="click-constrained-option",
    version=get_version(),
    description="Constrained option support for click",
    long_description=get_readme(),
    long_description_content_type="text/markdown",
    license="BSD",
    url="https://github.com/nobody-65534/click-constrained-option",
    packages=find_packages(),
    install_requires=["click>=7.0,<8"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8"
    ],
    python_requires='>=3.6'
)
