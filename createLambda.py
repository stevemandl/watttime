import boto3
iam_client = boto3.client('iam')
lambda_client = boto3.client('lambda')
#env_variables = dict() 

with open('lambda.zip', 'rb') as f:
    zipped_code = f.read()

role = iam_client.get_role(RoleName='LambdaBasicExecution')

kwargs = {
    'FunctionName': 'updateWatttime',
    'Runtime': 'python2.7',
    'Role': role['Role']['Arn'],
    'Handler': 'lambdaToRDS.handler',
    'Code': dict(ZipFile=zipped_code),
    'Timeout': 10, # 300 <seconds> is Maximum allowable timeout
    'VpcConfig': {
        'SubnetIds': ['subnet-86efa4ac','subnet-c2a07c8a'], 
        'SecurityGroupIds': ['sg-991937e2',]
    }
}

lambda_client.create_function( **kwargs )


