import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
    name="redditngram",
    version="0.0.1",
    author="Brian Li",
    author_email="zhenbangli@gmail.com",
    description="redditngram",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/boffee/redditngram-py",
    packages=setuptools.find_packages(),
    install_requires=[
      'tqdm',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)