from setuptools import setup, find_packages

import permitronix

setup(
    name='Permitronix',
    version=permitronix.ver,
    packages=find_packages(),
    url='https://github.com/hsn8086/Permitronix',
    license='MIT',
    author='hsn',
    author_email='hsn1919810@gmail.com',
    description='A py permission management module.',
    long_description=open('readme.md', 'r', encoding='utf8').read(),
    long_description_content_type='text/markdown'
)
