import setuptools

setuptools.setup(
    name='PrivateBinAPI',
    version="1.0.0",
    author="Pioverpie",
    description="A wrapper for the PrivateBin API",
    long_description='',
    long_description_content_type='text/markdown',
    url='',
    packages=['privatebinapi'],
    install_requires=['PBinCLI', 'requests', 'httpx']
)
