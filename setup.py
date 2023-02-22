from setuptools import setup,find_packages

import permitronix

setup(
    name='Permitronix',
    version=permitronix.ver,
    packages=find_packages(),
    url='https://github.com/hsn8086/Permitronix',
    license='MIT',
    author='hsn',
    install_requires=['RP-DataBase'],
    author_email='hsn1919810@gmail.com',
    description='A py permission management module.'
)
