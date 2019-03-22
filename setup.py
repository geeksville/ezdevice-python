import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="ezdevice",
    version="0.0.7",
    description="Python tool & library for using ESP32 based Ezdevice.net projects",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/geeksville/ezdevice-python",
    author="Kevin Hester",
    author_email="kevinh@geeksville.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["ezdevice"],
    include_package_data=True,
    install_requires=["esptool", "requests"],
    python_requires='>=3',
    entry_points={
        "console_scripts": [
            "ezdevice=ezdevice.__main__:main",
        ]
    },
)
