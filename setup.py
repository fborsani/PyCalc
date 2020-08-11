import pathlib

from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name="PyCalc",
    version="1.0",
    license="MIT",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(include=["PyCalc", "PyCalc.gui"]),
    install_requires=["bitstring", "PyQt5"],
    entry_points={'console_scripts': ['PyCalc=PyCalc.main:main']},
    include_package_data=True
)
