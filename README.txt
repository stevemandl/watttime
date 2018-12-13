Some useful commands:
cd watttime
source venv_lambda/bin/activate - activate virtualenv for testing lambdaToRDS.py
ll - shortcut for ls -la
python lambdaToRDS.py - test lambda function before updating it
deactivate - get out of the virtualenv environment
./create_zip.sh - (re)create the lambda zip file
python updateLambda.py - create or update the lambda function
aws lambda invoke --function-name updateWatttime out.txt
cat out.txt - look at the contents of out.txt

