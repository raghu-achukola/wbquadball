# wbquadball
Central mono-repo for all work undertaken to building apps, standardizing statistics, etc. for the sport of quadball.

Inc 1: 
Created "template" of functions- 
* repo structure, package, __init__s, setup.py, test folder, test data, requirements, .gitignore
* quadball package
   * setup.py 

Inc 2: 
* Repository: Created CI/CD workflow template
* Github: attached secrets for GHA_AWS_ACCESS_KEY and GHA_AWS_SECRET_ACCESS_KEY
* AWS: Create GH Actions IAM user and grant necessary permissions

Inc 3: 
* Installed protobuf v4.22.1 and added to requirements
* Setup protobuf project template
* Created protocompile.py file to automate compile of python files from protoschema
* Made schema folder a python package
* Added open_file() with eventual functionality to open both S3 and local files
* Added unit testing for schema compliance