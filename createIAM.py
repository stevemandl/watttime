import json, boto3
# From https://alestic.com/2014/11/aws-lambda-cli/

role_name = 'LambdaBasicExecution'
assume_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "",
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}


role_policy_document = {
    "Version": "2012-10-17",
    "Statement":{
        "Effect": "Allow",
        "Action": [
            "logs:CreateLogGroup",
            "logs:CreateLogStream",
            "logs:PutLogEvents",
            "ec2:CreateNetworkInterface",
            "ec2:DescribeNetworkInterfaces",
            "ec2:DeleteNetworkInterface"
        ],
        "Resource": "*"
    }
}

iam_client = boto3.client('iam')
resp = iam_client.create_role(
    RoleName=role_name,
    AssumeRolePolicyDocument=json.dumps(assume_policy),
)
print (resp)

resp2 = iam_client.put_role_policy(
    RoleName=role_name,
    PolicyDocument=json.dumps(role_policy_document),
    PolicyName='lambda-policy',
)
print(resp2)

