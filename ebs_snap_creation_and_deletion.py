from __future__ import print_function
import boto3
import time
from boto3 import resource
from datetime import timedelta, datetime
#'''
#    This script takes snapshot of volumes which are secondary volumes and are attached to instance having "Backup:true" tag
#'''
#Adding time function
current_time = time.gmtime()
ae = time.asctime(current_time)
#SNAPSHOT_TAGS = {'BackUp_Time': time.asctime(current_time) }
SNAPSHOT_TAGS = {'BackUp_Time': ae }    #Dictionary of tags to apply to the created snapshots
TAG_FILTERS = [{'Name': 'tag:BackUp','Values': ['Yes']}]   # Tags on which ec2 instance should get filter
REGION = "us-east-1"                                       # AWS region in which the volumes exist

def take_snapshots(volume, tags_kwargs):
    snapshot = volume.create_snapshot(
           Description='SR0022341-Jenkin_Server_Volume-BackUp'
           )
    #snapshot = ec2.create_snapshot(VolumeId=volume,Description='Created by Lambda function ebs-snapshots')
    print(snapshot)
    if tags_kwargs:
        snapshot.create_tags(**tags_kwargs)

def process_tags():
    tags = []
    tags_kwargs = {}
    # AWS allows 10 tags per resource
    if SNAPSHOT_TAGS and len(SNAPSHOT_TAGS) <= 30:
        for key, value in SNAPSHOT_TAGS.items():
            tags.append({'Key': key, 'Value': value})
            tags_kwargs['Tags'] = tags
    return tags_kwargs


def print_summary(counts):
    print("\nSUMMARY:\n")
    print("Snapshots created:  {}{}".format(counts,""))
    print("-------------------------------------------\n")


def lambda_handler(event, context):

    snap_count = 0

    # List of devices that should be consider to take snapshot. Root volume is excluded here i.e. /dev/xvda or /dev/sda
    DEVICES = ['/dev/sda1', '/dev/sdf']

    ec2 = resource("ec2", region_name=REGION)
    ec2_client = boto3.client('ec2')

    # Get information for all instances with tag "Backup:true"
    instances = ec2.instances.filter(Filters=TAG_FILTERS)

    # Filter all instances that have are attached to ec2 instances in "instances"
    for instance in instances:
        ec2_instance = ec2.Instance(instance.id)
        print("for instance:", ec2_instance )
        volumes = ec2.volumes.filter(Filters=[{'Name': 'attachment.instance-id', 'Values': [ec2_instance.id]}, {'Name': 'attachment.device', 'Values': DEVICES} ])
#volumes = ec2.volumes.filter(Filters=[{'Name': 'attachment.instance-id', 'Values': [ec2_instance.id]} ])
        #print(volumes)
  
        for tags in instance.tags:
            #print("inside for loop of instance.tags")
            if tags["Key"] == 'Name':
                SNAPSHOT_TAGS['Name'] = tags["Value"]

  
        # Take Backup
        for volume in volumes:
            tags_kwargs = process_tags()


            print("Taking snapshot..")
            take_snapshots(ec2.Volume(volume.id), tags_kwargs)
            snap_count += 1
            
    print("at last summary")
    print_summary(snap_count)
    
    
    
    
#-------------------------Deleting the ebs_volume as per the retention period in days that we set ---------------------#
days = 7

#filters = [{'SNAPSHOT_TAGS'}]
filters = [{'Name': 'tag:Name', 'Values': ['int-new-jenkins-m5.xlarge'] }]
ec2= boto3.setup_default_session(region_name='us-east-1')
client = boto3.client('ec2')
snapshots = client.describe_snapshots(Filters=filters)
for snapshot in snapshots["Snapshots"]:
    start_time = snapshot["StartTime"]
    delete_time = datetime.now(start_time.tzinfo) - timedelta(days=days)
    if start_time < delete_time:
            print('Deleting {id}'.format(id=snapshot["SnapshotId"]))
            client.delete_snapshot(SnapshotId=snapshot["SnapshotId"], DryRun=False)
