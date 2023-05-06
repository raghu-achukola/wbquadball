## Deploying Lambda: parse-statsheet
mkdir deploy_wbquadball-uw2-parse-statsheet
echo $1
cd deploy_wbquadball-uw2-parse-statsheet
cp ../../lambdas/wbquadball-uw2-parse-statsheet.py .
zip deploy_wbquadball-uw2-parse-statsheet.zip wbquadball-uw2-parse-statsheet.py
aws s3 cp deploy_wbquadball-uw2-parse-statsheet.zip s3://wbquadball-uw2-deployment/lambdas/deploy_wbquadball-uw2-parse-statsheet.zip
cd ..
rm -r deploy_wbquadball-uw2-parse-statsheet
aws lambda update-function-code --function-name wbquadball-uw2-parse-statsheet --s3-bucket wbquadball-uw2-deployment --s3-key lambdas/deploy_wbquadball-uw2-parse-statsheet.zip 
# Resource conflict exception will result due to simultaneous updates unless we wait until function updated
aws lambda wait function-updated --function-name wbquadball-uw2-parse-statsheet
aws lambda update-function-configuration --function-name wbquadball-uw2-parse-statsheet --layers $1
## TODO: rewrite in better format (take input parameters?)
## Deploying Lambda: register-entity
mkdir deploy_wbquadball-uw2-register-entity
echo $1
cd deploy_wbquadball-uw2-register-entity
cp ../../lambdas/wbquadball-uw2-register-entity.py .
zip deploy_wbquadball-uw2-register-entity.zip wbquadball-uw2-register-entity.py
aws s3 cp deploy_wbquadball-uw2-register-entity.zip s3://wbquadball-uw2-deployment/lambdas/deploy_wbquadball-uw2-register-entity.zip
cd ..
rm -r deploy_wbquadball-uw2-register-entity
aws lambda update-function-code --function-name wbquadball-uw2-register-entity --s3-bucket wbquadball-uw2-deployment --s3-key lambdas/deploy_wbquadball-uw2-register-entity.zip 
# Resource conflict exception will result due to simultaneous updates unless we wait until function updated
aws lambda wait function-updated --function-name wbquadball-uw2-register-entity
aws lambda update-function-configuration --function-name wbquadball-uw2-register-entity --layers $1
## TODO: Really find a better way to do this, we're just copy-pasting code now
## Deploying Lambda: roster-lookup
mkdir deploy_wbquadball-uw2-roster-lookup
echo $1
cd deploy_wbquadball-uw2-roster-lookup
cp ../../lambdas/wbquadball-uw2-roster-lookup.py .
zip deploy_wbquadball-uw2-roster-lookup.zip wbquadball-uw2-roster-lookup.py
aws s3 cp deploy_wbquadball-uw2-roster-lookup.zip s3://wbquadball-uw2-deployment/lambdas/deploy_wbquadball-uw2-roster-lookup.zip
cd ..
rm -r deploy_wbquadball-uw2-roster-lookup
aws lambda update-function-code --function-name wbquadball-uw2-roster-lookup --s3-bucket wbquadball-uw2-deployment --s3-key lambdas/deploy_wbquadball-uw2-roster-lookup.zip 
# Resource conflict exception will result due to simultaneous updates unless we wait until function updated
aws lambda wait function-updated --function-name wbquadball-uw2-roster-lookup
aws lambda update-function-configuration --function-name wbquadball-uw2-roster-lookup --layers $1