import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='dpdt',
    version='0.0.1',
    author='TimeWz667',
    author_email='TimeWz667@gmail.com',
    description='A small example package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/TimeWz667/PyDemography.git',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'scipy', 'numpy', 'pandas', 'request', 'wget'
    ],
    python_requires='>=3.7',
)
