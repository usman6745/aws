# aws
Repository contains_ lambda function codes in-order to backup the stack services as per the requests i have had gone through.

Requirement : Backup the ec2:instance server's EBS- VOLUMES (Root and all attached ebs volumes) using aws lambda function - which is having an access to ec2, aws-cloud-watch-logs and cloudwatch-events.

Resources: 
https://jee-appy.blogspot.com/2018/05/automated-ebs-volume-snapshot-lambda.html
(took the backup-ebs-vol code from this site as a first half)[(https://www.youtube.com/watch?v=I9E9F8HD_7E)]
http://tuxlabs.com/?p=626   (took the deletion/retention period code from the second half for my code)          
https://github.com/miztiik/serverless-backup   (not used- but for reference)
https://www.codebyamir.com/blog/automated-ebs-snapshots-using-aws-lambda-cloudwatch  (not used- but for reference)
