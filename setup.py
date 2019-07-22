import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, "bswtf", "__version__.py")) as f:
    exec(f.read(), about)

setup(
    name="bswtf",
    version=about["__version__"],
    description="WTForms for Boostrap",
    url="https://github.com/5uper5hoot/bswtf.git",
    author="Peter Schutt",
    author_email="peter@topsport.com.au",
    license='MIT License',
    packages=["bswtf"],
    install_requires=['markupsafe', 'wtforms']
)
