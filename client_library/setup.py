from setuptools import setup,find_packages


setup(name='SkyScribe',
      version='1.0.0',
      author = 'Brugnara-DelGrande',
      description='Application used to get relevant information about '
                  'the weather and interact with weather stations.',
      package_dir={"" : "."},
      packages= find_packages(),
      install_requires=['pandas','requests'],
      python_requires=">=3.10")