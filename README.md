# serverless-fortune-sms

This is an [AWS Lambda](https://aws.amazon.com/lambda/) function that implements a simple [`fortune`](https://en.wikipedia.org/wiki/Fortune_(Unix)) program, like those inclided on many Unixes. Using [Amazon Simple Notification Service](https://aws.amazon.com/sns/), it is able to send an SMS each day to a pre-configured phone number, containing a randomly selected fortune from its database.

The `fortunes` included as a sample here come from Plan 9's [`/lib/fortunes`](https://github.com/9fans/plan9port/blob/master/lib/fortunes), which is covered by the [Lucent Public License](https://github.com/9fans/plan9port/blob/master/LICENSE).

Please note that [SNS only supports SMS messaging in a subset of regions](http://docs.aws.amazon.com/sns/latest/dg/sms_supported-countries.html). Please see the linked support document to ensure you deploy this application in a supported region.

## Deployment

Deploying this serverless app to your AWS account is quick and easy using [AWS CloudFormation](https://aws.amazon.com/cloudformation/). 

### Packaging

With the [AWS CLI](https://aws.amazon.com/cli/) installed, run the following command to upload the code to S3. You need to re-run this if you change the code in `archiver.py`. Be sure to set `DEPLOYMENT_S3_BUCKET` to a **bucket you own**; CloudFormation will copy the code function into a ZIP file in this S3 bucket, which can be deployed to AWS Lambda in the following steps. 

```sh
DEPLOYMENT_S3_BUCKET="YOUR_S3_BUCKET"
aws cloudformation package --template-file cloudformation.yaml --s3-bucket $DEPLOYMENT_S3_BUCKET \
  --output-template-file cloudformation-packaged.yaml
```

Now you will have `cloudformation-packaged.yaml`, which contains the full path to the ZIP file created by the previous step. 

### Configuring

Next, let's set the required configuration. You can set the following parameters:
 
 * `STACK_NAME` is the name of the CloudFormation stack that you'll create to manage all the resources (Lambda functions, CloudWatch Events) associated with this app. You can set this to a new value to create a new instance with different parameters in your account, or use the same value when re-running to update parameters of an existing deployment.
 * `PHONE_NUMBER` is the recipient of the daily fortune. Use [E.164](https://en.wikipedia.org/wiki/E.164) (e.g. +15555550100) format.
 * `UTC_HOUR` is the UTC hour at which to send the fortune.

```sh
STACK_NAME="serverless-fortune-sms"
PHONE_NUMBER="+12068007270"
UTC_HOUR="10"
```

With these configuration parameters defined, we can call `cloudformation deploy` to create the necessary resources in your AWS account:

```sh
aws cloudformation deploy --template-file cloudformation-packaged.yaml --capabilities CAPABILITY_IAM --parameter-overrides \
  "PhoneNumber=$PHONE_NUMBER" \
  "UTCHour=$UTC_HOUR" \
  --stack-name $STACK_NAME
````

If all went well, your stack has now been created. Next time the clock strikes `$UTC_HOUR`, you should look forward to a fortune at `$PHONE_NUMBER`!
