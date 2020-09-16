import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='simulite',
    version='1.1.1',
    author='wolray',
    author_email='wolray@foxmail.com',
    description='A simple and flexible event-based simulator',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/wolray/simulite',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
