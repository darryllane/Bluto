from setuptools import setup, find_packages

setup(
    name='Encryption',
    version='0.1b.0dev',
    author='Darryl lane',
    author_email='DarrylLane101@gmail.com',
    packages=['Encryption'],
    include_package_data=True,
    license='LICENSE.txt',
    description='''
    Create encrypted data in a file, and test decrypt.
    ''',
    long_description=open('README.md').read(),
    
    scripts=['risk_user_check.py'],
    install_requires=[
        "Fernet",
        "argparse",
    ],
)

