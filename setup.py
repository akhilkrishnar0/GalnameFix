from setuptools import setup, find_packages

setup(
    name="galnamefix",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "astropy",
        "astroquery"
    ],
    python_requires='>=3.11',
)

