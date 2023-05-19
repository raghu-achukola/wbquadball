
from setuptools import setup, find_packages

setup(
    #this will be the package name you will see, e.g. the output of 'conda list' in anaconda prompt
    name = 'quadball', 
    #some version number you may wish to add - increment this after every update
    version='0.0.24', 
  
    packages=find_packages(), #include/exclude arguments take * as wildcard, . for any sub-package names
    include_package_data=True,
    package_data={'': ['resources/statsheet/*.xlsx']}
)