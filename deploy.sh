
set -e

STACK_NAME="api-sfs-proto"
CF_BUCKET_NAME=${CF_BUCKET_NAME}

function package(){
	aws cloudformation package --template-file stack.yaml --s3-bucket $1 --output-template-file .packaged-template.yaml	
}

function deploy(){
	aws cloudformation deploy --template-file .packaged-template.yaml --stack-name $1 --capabilities CAPABILITY_IAM
}


echo "Packaging stack ..."

package $CF_BUCKET_NAME

echo "Deploying stack ..."

deploy $STACK_NAME 
