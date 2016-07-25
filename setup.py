from setuptools import setup

setup(
    name='cloudflare_stun',
    version='0.1dev1',
    packages=['cloudflare_stun'],
    license='MIT',
    long_description=open('README.md').read(),
    install_requires=open('requirements.txt').read().split(),
    entry_points={
        'console_scripts': [
            'cloudflare_stun = cloudflare_stun:App.main',
        ]
    }
)
