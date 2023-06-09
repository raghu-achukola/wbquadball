mkdir deploy_quadball/
cd deploy_quadball/
mkdir python
cd python
pip install -r ../../../requirements.txt -t .
pip install ../../../ -t .
cd ..
zip -r deploy_quadball.zip .
aws s3 cp deploy_quadball.zip s3://wbquadball-uw2-deployment/layers/deploy_quadball.zip
cd ..
rm -r deploy_quadball/
aws lambda publish-layer-version --layer-name quadball --content S3Bucket=wbquadball-uw2-deployment,S3Key=layers/deploy_quadball.zip