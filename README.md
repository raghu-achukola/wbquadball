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


Inc 4: 
* AWS: Created S3 bucket s3://wbquadball-uw2-deployment to host all deployment artefacts
* Created lambdas/ folder which will host lambda code
* Created a deploy/ folder which will host shell scripts to deploy code upon merge
* deploy_lambdas.sh currently uploads the lone lambda to S3 
* Modify GHA on merge to main runs deploy_lambdas .sh