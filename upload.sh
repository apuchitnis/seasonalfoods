#!/bin/bash

pushd ./venv/lib/python3.7/site-packages/
zip -r9 ../../../../seasonalfoods.zip .
popd
zip -g seasonalfoods.zip *.py

aws s3 cp seasonalfoods.zip s3://seasonalfoods
aws lambda update-function-code --function-name=seasonalfoods --s3-bucket=seasonalfoods --s3-key=seasonalfoods.zip --publish

rm seasonalfoods.zip
