import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zabbix-jolokia",
    version="0.0.1",
    author="Sven Hergenhahn",
    author_email="sven.hergenhahn@dm.de",
    description="A module to read from jolokia endpoints and return json - ready for use with zabbix",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/svenXY/zabbix-jolokia",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)

