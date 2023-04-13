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
