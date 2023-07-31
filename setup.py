from setuptools import setup, find_packages

setup(
    name="hpdag",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        "networkx",

    ],
    author="Ohad Rubin",
    description="A DAG library to manage hyperparameter search and ablations",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/OhadRubin/hpdag",
)