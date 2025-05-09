## here I have covered how to delete the stale resources and get the details on your email id. This will be fully automated project no human intervention.
## follow the steps to build this project which will help you a lot as well as to your organization to whom you are working or in future you are going to work.


## step1. create a lambda function using the code which are provided in this file. This will delete the stale resources which are older than seven days.
## step2. change the line no 28 based on your sns topic arn
## step3. make sure to attach IAM role which have the access of ec2 instances describe, snapshots describe, volumes describe, cloudwatch full access, sns full acess to your lambda function.
## step4. create a sns topic/subscription which will send the notification based on your configuration.
## step5. check the email id which you have given in sns subscription and subscribe that.
## step6. create a aws eventbridge which will help you to trigger this lambda function on your behalf based on your timing and configuration.
## step7. once successfully deploy this project check your mail box whether you are getting the email or not. 

import boto3
import datetime

# AWS Clients
ec2_client = boto3.client('ec2')
sns_client = boto3.client('sns')
sts_client = boto3.client('sts')

# Threshold for stale resources (in days)
DAYS_THRESHOLD = 7

# Get AWS Account ID and Region dynamically
aws_account_id = sts_client.get_caller_identity()['Account']
aws_region = boto3.session.Session().region_name

SNS_TOPIC_ARN = f"arn:aws:sns:{aws_region}:{aws_account_id}:your-sns-topic"

def lambda_handler(event, context):
    deleted_volumes = []
    deleted_snapshots = []

    # Get current date
    today = datetime.datetime.utcnow()

    # Identify & Delete Orphaned EBS Volumes
    volumes = ec2_client.describe_volumes()['Volumes']
    for volume in volumes:
        if not volume['Attachments']:  # Only consider unattached volumes
            create_time = volume['CreateTime'].replace(tzinfo=None)
            if (today - create_time).days > DAYS_THRESHOLD:
                deleted_volumes.append(volume['VolumeId'])
                
                # Delete volume
                ec2_client.delete_volume(VolumeId=volume['VolumeId'])

    # Identify & Delete Stale Snapshots
    snapshots = ec2_client.describe_snapshots(OwnerIds=['self'])['Snapshots']
    for snapshot in snapshots:
        start_time = snapshot['StartTime'].replace(tzinfo=None)
        if (today - start_time).days > DAYS_THRESHOLD:
            deleted_snapshots.append(snapshot['SnapshotId'])
            
            # Delete snapshot
            ec2_client.delete_snapshot(SnapshotId=snapshot['SnapshotId'])

    # Notify via SNS
    if deleted_volumes or deleted_snapshots:
        message = f"Deleted Stale Resources:\nVolumes: {deleted_volumes}\nSnapshots: {deleted_snapshots}"
        sns_client.publish(TopicArn=SNS_TOPIC_ARN, Message=message, Subject="AWS Stale Resource Cleanup Notification")

    return {
        "deleted_volumes": deleted_volumes,
        "deleted_snapshots": deleted_snapshots
    }
