from setuptools import setup, find_packages
import os
import codecs

HERE = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    """
    Build an absolute path from *parts* and and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    with codecs.open(os.path.join(HERE, *parts), "rb", "utf-8") as f:
        return f.read()

setup(
    name='cloudflare_stun',
    version='0.1dev2',
    packages=find_packages(),
    license='MIT',
    description="CloudFlare Dynamic DNS using STUN",
    long_description=read('README.rst'),
    install_requires=read('requirements.txt').split(),
    author="Will Hughes",
    author_email="will@willhughes.name",
    url="https://github.com/insertjokehere/cloudflare-stun",
    entry_points={
        'console_scripts': [
            'cloudflare_stun = cloudflare_stun:App.main',
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 2 :: Only",
        "Programming Language :: Python :: 2.7",
        "Topic :: Internet :: Name Service (DNS)",
    ]
)
