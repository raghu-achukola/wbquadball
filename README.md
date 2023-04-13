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
* AWS : Created Lambda function wbquadball-uw2-parse-statsheet
* Created lambdas/ folder which will host lambda code
* Created a deploy/ folder which will host shell scripts to deploy code upon merge
* deploy_lambdas.sh currently uploads the lone lambda to S3 and updates the Lambda function
* Modify GHA workflow on merge to main runs deploy_lambdas.sh

Inc 5: 
* Create method that yields each possession block in a stats worksheet
* Create method that yields each StatSheetPossession object
* NOTE: tech debt incurred, testing not complete for generator objects as framework for storing data/fixtures for unit tests not present

Inc 6: 
* AWS S3: Create layer/ path where lambda layer deployments will live
* CI/CD: Create a deploy_layer.sh file to run before deploy_lambdas that will generate a package zip full of quadball/ and all dependencies and upload to S3
* AWS Lambda: Create a layer quadball with initial code found in the S3 file
* CI/CD: Modify deploy_layer.sh to update quadball lambda layer with latest code on merge to main 
* CI/CD: Modify deploy_lambdas.sh to 
   a\ update the function code with latest lambda code 
   b\ WAIT until the update has completed
   c\ attach the latest version of the lambda layer
* Modify existing lambdas to do a empty import of quadball package to test lambda function-layer connectivity

Inc 7: 
* Data Model: Added the structure for the central OLTP data model, with first message type (Possession)
* Unit Testing: Added unit tests/test data for new data model 
