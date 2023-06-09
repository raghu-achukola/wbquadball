# wbquadball
Central mono-repo for all work undertaken to building apps, standardizing statistics, etc. for the sport of quadball.

## AWS Architecture Diagram
![AWS Architecture Diagram](aws_architecture.png)

## Incremental Change Log
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

Inc 8: 
* AWS Lambda: Update Lambda to have a function to do act on an S3 Trigger framework. (temporary) 
* AWS Lambda: Update Lambda to have a timeout of 1 min instead of 3 sec
* AWS S3: Create landing bucket for AWS Lambda (temporary)
* AWS Lambda/IAM : Update Lambda permissions to be able to access S3 bucket ^ 
* Code Lambda: Update Lambda code to read in the xlsx file caused by the trigger, parse into Statsheet objects, and print
* Quadball package: Fix statsheet gen_possessions bug


Inc 9: 
* quadball.db: Begin conversion package from statsheet -> central data model, starting with the Extra message
* Unit testing: add unit tests for new conversion code for Extra message
* Code Lambda: Update Lambda code to test this extra parsing functionality


Inc 10: 
* quadball.db: Add functionality to the conversion package, converting whole Possessions
* Unit testing: add unit tests for new conversion code for Possession
* Code Lambda: Update Lambda code to test full possession reading from statsheet

Inc 11: 
* models.quadball.db: Added canonical representation of a Game () objecte. The flow will work like this. We except Game objects to be created ahead of time (doc db? json? ) but empty. The Game value will thn contain the information necessary 
* quadball.db.game/ rulesets: Added functionalities to parse entire games 
* Unit testing: Unit testing on all of this ^ 
 
Inc 12: 
Through development of just Game() class, we realized we need database read/write
to handle complex things like player lookup and tournmanet/season/ruleset/etc. 
* models.quadball.db: Added canonical representation of League, Season, Tournament, Team, Player
* MongoDB: started mongodb cluster quadball-stats

Inc 13 (Pure Console): 
* Created read-write user for the API to use in MongoDB Atlas console 
and stored credentials in AWS Secrets Manager
* Created Lambda in AWS Console  wbquadball-uw2-register-entity that just has empty shell (returns event )    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }
* Created API Gateway Quadball Stats REST API 
* Create resource /quadball-stats, subresource /quadball-stats/register-entity, enable Lambda proxy on  route /quadball-stats/register-entity/{proxy+}
* Test to capture request format from request:
/quadball-stats/register-entity/league?object=%7B%22sup%22:2%7D
(found in test_data)


Inc 14
* Granted the API (specifically the role used by the lambda triggered by the API) access to the mongo db secret
* Modify lambda code to make a connection to the MongoDB
* Include CI/CD for new API lambda

Inc 15
* Make the lambda code actually REGISTER the entity and return entity

Inc 16
* Add the ability to register players
* Load the DB with pre-existing players and teams
* Add lookup functionality to the statsheet converter
* Update the db models that correspond to Mongo Collections to have _id fields 

Inc 17
* API/REGISTER: Add a duplicate condition -> if secondary id is a duplicate, the API will not write the duplicate
* LAMBDA/register-entity: Update Lambda for register-entity API to propagate new format
* MODELS/db : Move Ruleset to be defined at the Season level. This is just code location switching for now, will eventually turn into ruleset being defined AT the season level and GameParser taking the ruleset from the Season object
* QUADBALL/db : Rewrite imports to adjust for the models change

Inc 18
* MONGODB/IAM: Create new read-only user for MongoDB for public facing APIs and read-only APIs
* AWS/SecretsManager: Create secret mirroring keys in secret in Inc 13
* QUADBALL/db/api: Add roster_lookup functionality
* AWS/Lambda: Created lambda wbquadball-uw2-roster-lookup, with environment variable 
pointing to Secret ^.
* AWS/IAM: Modify the Lambda role ^ to be able to access the new secret
* AWS/API Gateway: Setup /roster-lookup resource, and add a GET method that calls ^ that lambda
* CI/CD : Add deployment of wbquadball-uw2-roster-lookup w quadball layer 

* Tech Debt: note, we are overlevered
  * add unit testing for lambdas/api 
  * refactor shell scripts for CI/CD to functionalize deployment process


Inc 19
* AWS/Lambda: Alter environment variables for parse-statsheet to include DB API URL 
* AWS/Lambda: Created lambda wbquadball-uw2-validate-game-metadata
* CI/CD: Deploy lambda wbquadball-uw2-validate-game-metadata
* AWS/API Gateway: Created API resource validate-game-metadata
   * Added Trigger to GET method to call above Lambda
* Templates/live-stats.xlsx: Standardize template for stat taking
* Lambdas/parse-statsheet: 
   * Read all three worksheets
   * Use Roster Lookup API  to validate the ROSTERS Worksheet



Inc 20
* Unit Testing/quadball.db: Add test data for all objects to validate schema and test backcompatibility
* Quadball/statsheet : Docstrings for all functions in statsheet converter
* models/ : Entity Relationship Diagram + summary for DB and STATSHEET domains

Inc 21
* Quadball/db : Change API to multithread the roster lookup to speed up retrieval 

Inc 22
* Quadball/db : Add api-reload-game functionality 
* Lambdas/api-reload-game:   Add api-reload-game lambda functionality
* AWS/API Gateway: Created API resource api-reload-game
   * Added Trigger to GET method to call above Lambda
* AWS/Lambda: Create lambda wbquadball-uw2-api-reload-game
* CI/CD: Refactor CI/CD to modularize each deployment (using the same code to deploy all lambdas rather than copy-pasting)
* AWS/IAM: Create policy to give access to a mongo-rw role in AWS and attach policy to lambda execution role

Inc 23
* App:   Basic (super-basic) template for a Flask App with a form frontend to download/ upload statsheets 

Inc 24
* App/JS:      Add to the template to expect input data in the canonical data model format. The Flask application will then allow the user to select any of the existing games and existing games only. 
* App/Python:  use openpyxl to prepare the excel template inserting team names and team ids and then allowing a download of the formatted spreadsheet

Inc 25
* AWS/S3: Create S3 bucket wbquadball-uw2-public-metadata-storage. Exports will be located in this S3 Bucket. For all data that doesn't need near-real-time updates, this S3 access will provide a much cheaper data access model than querying MongoDB itself. Alter the bucket policy to allow public read (but not public write) access.  
* AWS/Lambda : Create lambda wbquadball-uw2-nightly-db-public-export. The lambda handler will export the registrable collections (league, season, team, game, tournament) to json files in the S3 bucket. 
* AWS/Lambda or Eventbridge: Create crontab schedule to run the export lambda every day at 6 AM UTC
* AWS/IAM: Create policy to give access to a mongo-ro role in AWS and attach policy to lambda execution role


Inc 26 
* App: Alter app to use the S3 public URL 

Inc 27
* AWS/Lambda: Attach IAM policy that gives rw access to the public metadata storage bucket to parse-statsheet
* Lambdas/parse-statsheet: Modify code to reload game
* Lambdas/parse-statsheet: Modify code to store the uploaded statsheet with as {game_id}.xlsx in the public metadata storage bucket, and pass on this public http link to be used as game.stats_source
* quadball/db: Modify game parser to attach stats_source on each possession from a game_template Game object
* APIs/api-reload-game: Modify structure of API method to be a PUT request with the possessions as the data (following best practice, plus impossible to transmit all possession data in a GET request) and to take game-template as an query string parameter
* Lambdas/api-reload-game: Modify code to update game with film links from statsheet and statsource from S3
* README: add AWS Architecture Diagram