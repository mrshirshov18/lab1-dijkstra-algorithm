from setuptools import setup, find_packages

setup(
    name="dijkstra-algorithm",
    version="1.0.0",
    description="An implementation of Dijkstra's algorithm in Python",
    author="Maks Shirshov",
    author_email="shms2003@yandex.ru",
    packages=find_packages(),
    install_requires=[
        "networkx>=2.0",
    ],
)
