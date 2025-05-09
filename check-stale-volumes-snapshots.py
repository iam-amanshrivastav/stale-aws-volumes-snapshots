## here I have covered how to get the stale resources details daily on your email id. This will be fully automated project no human intervention.
## follow the steps to build this project which will help you a lot as well as to your organization to whom your are working or in future you are going to work.


## step1. create a lambda function using the code which are provide in this file.
## step2. change the line no 40 based on your sns topic arn
## step3. make sure to attach IAM role which have the access of ec2 instances describe, snapshots describe, volumes describe, cloudwatch full access, sns full acess to your lambda function.
## step4. create a sns topic/subscription which will send the notification based on your configuration.
## step5. check the email id which you have given in sns subscription and subscribe that.
## step6. create a aws enentbridge which will help you to trigger this lambda function on your behalf based on your timing and configuration.
## step7. once successfully deploy this project check your mail box whether you are getting the email or not. 

## You will get the email on your email id if there is any stale resources found. if there is no any stale resource you will get the mail with message = "Your account is in a very good state as there are no stale resources."

import boto3
import datetime

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    sns = boto3.client('sns')

    seven_days_ago = datetime.datetime.utcnow() - datetime.timedelta(days=7)

    # Get unattached volumes
    volumes = ec2.describe_volumes(Filters=[{'Name': 'status', 'Values': ['available']}])['Volumes']
    stale_volumes = [v['VolumeId'] for v in volumes if v['CreateTime'].replace(tzinfo=None) < seven_days_ago]

    # Get old snapshots
    snapshots = ec2.describe_snapshots(OwnerIds=['self'])['Snapshots']
    stale_snapshots = [s['SnapshotId'] for s in snapshots if s['StartTime'].replace(tzinfo=None) < seven_days_ago]

    # Check if there are stale resources
    if not stale_volumes and not stale_snapshots:
        message = "Your account is in a very good state as there are no stale resources."
    else:
        message = f"Stale Resources Found:\nVolumes: {stale_volumes}\nSnapshots: {stale_snapshots}"

    # Send to SNS
    sns.publish(
        SNS_TOPIC_ARN = "arn:aws:sns:your-region:your-account-id:your-sns-topic",
        Message=message,
        Subject="AWS Stale Resources Alert"
    )

    return {"Volumes": stale_volumes, "Snapshots": stale_snapshots, "Message": message}
