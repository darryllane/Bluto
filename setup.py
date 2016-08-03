from setuptools import setup, find_packages

setup(
    name='Bluto',
    version='2.3.5',
    author='Darryl lane',
    author_email='DarrylLane101@gmail.com',
    url='https://github.com/darryllane/Bluto',
    packages=['Bluto'],
    py_modules = ['modules'],
    include_package_data=True,
    license='LICENSE.txt',
    description='''
    DNS Recon | Brute Forcer | DNS Zone Transfer | DNS Wild Card Checks
    DNS Wild Card Brute Forcer | Email Enumeration | Staff Enumeration
    Compromised Account Checking''',
    long_description=open('README.md').read(),
    scripts=['Bluto/bluto'],
    install_requires=[
        "dnspython",
        "termcolor",
        "BeautifulSoup4",
        "requests",
        "pythonwhois",
        "lxml",
        "oletools",
        "pdfminer",
    ],
)

