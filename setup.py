from distutils.core import setup

setup(
    name='mediaspider',
    version='0.0.4',
    author='Hendrik Langer',
    author_email='dev@h3ndrik.de',
    packages=['mediaspider', 'mediaspider.test'],
    scripts=['bin/crawler','bin/webui'],
    url='http://h3ndrik.de/projects/mediaspider/',
    license='LICENSE.txt',
    description='Multimedia-file crawler and webfrontend.',
    long_description=open('README.txt').read(),
    install_requires=[
        "sqlalchemy",
        "argparse",
        "bottle",
    ],
)
