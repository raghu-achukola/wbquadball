mkdir deploy_wbquadball-uw2-parse-statsheet
cd deploy_wbquadball-uw2-parse-statsheet
cp ../../lambdas/wbquadball-uw2-parse-statsheet.py .
zip deploy_wbquadball-uw2-parse-statsheet.zip wbquadball-uw2-parse-statsheet.py
aws s3 cp deploy_wbquadball-uw2-parse-statsheet.zip s3://wbquadball-uw2-deployment/lambdas/deploy_wbquadball-uw2-parse-statsheet.zip
cd ..
rm -r deploy_wbquadball-uw2-parse-statsheet
aws lambda update-function-code --function-name wbquadball-uw2-parse-statsheet --s3-bucket wbquadball-uw2-deployment --s3-object lambdas/deploy_wbquadball-uw2-parse-statsheet.zip