import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="andy_fraud",
    version="1.0.1",
    author="Arraying",
    author_email="paul.huebner@googlemail.com",
    description="Anti-typosquatting suite",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Arraying/Andy",
    project_urls={
        "Bug Tracker": "https://github.com/Arraying/Andy/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=["andy"],
    install_requires=[
        "tldextract",
        "jsonschema"
    ],
    python_requires=">=3.8",
)
