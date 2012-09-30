from distutils.core import setup

setup(
    author='Max Lincoln',
    author_email='max@devopsy.com',
    url='https://github.com/maxlinc/cfsync',
    name='cfsync',
    version='0.1dev',
    packages=['cfsync',],
    license='TBD',
    long_description=open('README.txt').read(),
    install_requires=[
	            "python-cloudfiles >= 1.1.10"
    ]
)
