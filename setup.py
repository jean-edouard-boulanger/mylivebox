import pathlib
import setuptools

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setuptools.setup(
    name='mylivebox',
    version="0.0.1",
    description="Access Livebox data and perform basic operations",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Jean-Edouard Boulanger",
    url="https://github.com/jean-edouard-boulanger/mylivebox",
    author_email="jean.edouard.boulanger@gmail.com",
    license="MIT",
    packages=["mylivebox"],
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
