import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="spyking-pkg-sweetdreams",
    version="0.0.1",
    author='SweetDreams',
    author_email='',
    description='package created for my research lab to simulate spiking neural networks',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https:github.com/CosmicSurgery/spyking',
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy',
        'pandas',
    ]
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent"
    ]
)
