## Deploying Lambda:
DEPLOY_DIR="deploy_${1}"
ZIP_DIR="${DEPLOY_DIR}.zip"
S3_PATH="s3://wbquadball-uw2-deployment/lambdas/${ZIP_DIR}"
LAMBDA_PATH="../../lambdas/${1}.py"

echo "DEPLOYING LAMBDA : ${1} with attached layer ${2}"
mkdir $DEPLOY_DIR
cd $DEPLOY_DIR
cp $LAMBDA_PATH .
zip $ZIP_DIR "${1}.py"
aws s3 cp $ZIP_DIR $S3_PATH
cd ..
rm -r $DEPLOY_DIR
aws lambda update-function-code --function-name $1 --s3-bucket wbquadball-uw2-deployment --s3-key "lambdas/${ZIP_DIR}"
# Resource conflict exception will result due to simultaneous updates unless we wait until function updated
aws lambda wait function-updated --function-name $1
aws lambda update-function-configuration --function-name $1 --layers $2