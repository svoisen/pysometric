from setuptools import setup

setup(
    name='pysometric',
    version='0.0.1',
    description='Isometric SVG drawing library.',
    author='Sean Voisen',
    author_email='sean@voisen.org',
    url='https://github.com/svoisen/pysometric',
    packages=['pysometric'],
    requires=['shapely', 'numpy']
)