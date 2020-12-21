import setuptools

with open('README.rst') as file:
    long_description = file.read()

setuptools.setup(
    name='PrivateBinAPI',
    version='1.0.0',
    author='Pioverpie',
    description='A wrapper for the PrivateBin API',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/Pioverpie/privatebin-api/',
    packages=['privatebinapi'],
    install_requires=['PBinCLI', 'requests', 'httpx'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Security :: Cryptography',
    ],
    keywords='privatebin pastebin',
    project_urls={
        'Source': 'https://github.com/Pioverpie/privatebin-api/',
        'Issues': 'https://github.com/Pioverpie/privatebin-api/issues/'
    },
    python_requires='>=3.6',
)
