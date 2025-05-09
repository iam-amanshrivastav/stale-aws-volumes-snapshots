# AWS Stale Resource Management

## 📌 Overview
This repository contains two AWS Lambda functions to efficiently manage stale AWS resources (EBS volumes & snapshots):

1. *Check Stale Resources: Identifies unattached EBS volumes & stale snapshots older than **7 days*.
2. *Delete Stale Resources*: Finds and deletes these stale resources automatically.

Both functions integrate *Amazon SNS*, notifying account owners of detected or deleted resources.

---

## 🛠 Project 1: Identify Stale EBS Volumes & Snapshots

### 🔹 Description
This AWS Lambda function automatically scans your AWS account to detect:
- *Unattached EBS volumes* older than *7 days*
- *Snapshots* older than *7 days*

The detected resources are then sent via *Amazon SNS* to alert the account owner.

### 🔹 Technologies Used
- *AWS Lambda* (Python)
- *Amazon EC2 (EBS & Snapshots)*
- *Amazon SNS* (Email notifications)
- *Amazon Eventbridge* (For scheduling)

### 🔹 Implementation Steps
1. Create an *IAM role* with necessary permissions.
2. Deploy the *Lambda function* with the provided Python script.
3. Create an *SNS topic* for email alerts.
4. Schedule execution using *Amazon Eventbridge*.

### 🔹 Lambda Function Behavior
- Fetches AWS *Account ID* and *Region dynamically*.
- Lists *unattached EBS volumes* older than *7 days*.
- Lists *snapshots* older than *7 days*.
- Sends a notification with resource details to *SNS*.
- Returns *stale resource IDs* as output.

---

## 🛠 Project 2: Delete Stale EBS Volumes & Snapshots

### 🔹 Description
This AWS Lambda function *automatically deletes*:
- *Unattached EBS volumes* older than *7 days*
- *Snapshots* older than *7 days*

Once deleted, it sends a notification via *Amazon SNS* to confirm the cleanup.

### 🔹 Technologies Used
- *AWS Lambda* (Python)
- *Amazon EC2 (EBS & Snapshots)*
- *Amazon SNS* (Email notifications)
- *Amazon Eventbridge* (For scheduling)

### 🔹 Implementation Steps
1. Create an *IAM role* with necessary permissions.
2. Deploy the *Lambda function* with the provided Python script.
3. Create an *SNS topic* for cleanup alerts.
4. Schedule execution using *Amazon Eventbridge*.

### 🔹 Lambda Function Behavior
- Fetches AWS *Account ID* and *Region dynamically*.
- Identifies *unattached EBS volumes* older than *7 days* and *deletes* them.
- Identifies *snapshots* older than *7 days* and *deletes* them.
- Sends a notification with *deleted resource IDs* to *SNS*.
- Returns *deleted resource IDs* as output.

---

## 📩 AWS SNS Configuration
Both Lambda functions use *Amazon SNS* for notifications.  
Ensure:
- An *SNS topic* is created.
- The *account owner's email* is subscribed.
- Proper *IAM permissions* are granted for *SNS publishing*.

---


