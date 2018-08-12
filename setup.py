import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-tuya-oittm",
    version="0.0.1",
    author="Supermotal",
    author_email="supermortaldns@gmail.com",
    description="A package for communicating with Tuya/Oittm devices on a local network.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Supermortal/python-tuya-oittm",
    packages=setuptools.find_packages(),
    install_requires=[
        'pycryptodome',
    ],
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ),
)
