import setuptools


setuptools.setup(
    name='mylivebox',
    version="0.0.1",
    description="Unofficial livebox API",
    author="Jean-Edouard Boulanger",
    author_email="jean.edouard.boulanger@gmail.com",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=[
        "requests",
    ]
)
