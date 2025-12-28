"""Setup script for RPi.GPIO stub package"""

from setuptools import setup

setup(
    name="RPi.GPIO-stub",
    version="0.1.0",
    description="Stub package for RPi.GPIO - development only",
    packages=["RPi"],
    package_dir={"RPi": "RPi"},
    install_requires=[],
    python_requires=">=3.6",
)

