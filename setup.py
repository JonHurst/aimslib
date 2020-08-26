import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aimslib",
    version="0.2",
    author="Jon Hurst",
    author_email="jon.a@hursts.org.uk",
    description="A library for working with AIMS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JonHurst/aimslib",
    packages=setuptools.find_packages(),
    install_requires=['Beautifulsoup4', 'requests', 'python-dateutil'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
