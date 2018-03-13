from setuptools import setup, find_packages

setup(
    name='Bluto',
    version='3.0b.0dev',
    author='Darryl lane',
    author_email='DarrylLane101@gmail.com',
    packages=['Bluto'],
    include_package_data=True,
    license='LICENSE.txt',
    description='''
    DNS Recon | Brute Forcer | DNS Zone Transfer | DNS Wild Card Checks
    DNS Wild Card Brute Forcer | Staff Enumeration
    ''',
    long_description=open('README.md').read(),
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/darryllane/Bluto/issues',
        'Vote': 'https://n0where.net/dns-analysis-tool-bluto',
        'Say Thanks!': 'http://saythanks.io/to/example',
        'Source': 'https://github.com/darryllane/Bluto',
	},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: UAT',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3.6',
	],
    scripts=['Bluto/bluto'],
    install_requires=[
        "dnspython",
        "termcolor",
        "BeautifulSoup4",
        "requests[security]",
        "pythonwhois",
        "lxml",
        "oletools",
        "pdfminer"
    ],
)

