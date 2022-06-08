import boto3
import base64
from botocore.exceptions import ClientError
with open("userdata.txt", "r") as fp:
 USERDATA_B64_STR = fp.read()
class CreateInstanceEC2(object):
 def __init__(self, ec2_client):
 self.ec2_client=ec2_client
#Security group
 def create_security_group(self):
 response = self.ec2_client.describe_vpcs()
 vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')
 response = self.ec2_client.create_security_group(GroupName='Secured_gr>
 Description='This is secured',
 VpcId=vpc_id)
 security_group_id = response['GroupId']
 print('Security Group Created %s in vpc %s.' % (security_group_id, vpc>
 data = self.ec2_client.authorize_security_group_ingress(
 GroupId=security_group_id,
 IpPermissions=[
 {'IpProtocol': 'tcp',
 'FromPort': 80,
 'ToPort': 80,
 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
 {'IpProtocol': 'tcp',
 'FromPort': 22,
 'ToPort': 22,
 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
 ])
 print('Ingress Successfully Set %s' % security_group_id)
 return security_group_id
#Lanuch template
 def create_ec2_launch_template(self):
 print("Creating the Launch Templates : STARTED ")
 security_group_id = self.create_security_group()
try:
 response = self.ec2_client.create_launch_template(
 LaunchTemplateName= 'launch_template',
 LaunchTemplateData={
 'ImageId': 'ami-0dc2d3e4c0f9ebd18',
 'InstanceType' : "t2.micro",
 'KeyName' : "ec2_keypair",
 'UserData': USERDATA_B64_STR,
 'SecurityGroupIds': [security_group_id]
 }
 )
 template_id = response['LaunchTemplate']['LaunchTemplateId']
 print("Creating the Launch Templates : COMPLETED : TemplateID"
 return template_id
 except Exception as e:
 print(e)
#Autoscaling group
 def create_ec2_auto_scaling_group(self):
 print ("---- Started the creation of Auto Scaling Group using Launch T>
 template_id = self.create_ec2_launch_template()
 client = boto3.client('autoscaling',)
 response = client.create_auto_scaling_group(
 AutoScalingGroupName='autoscaling_group',
 LaunchTemplate={
 'LaunchTemplateId': template_id,
 },
 MinSize=2,
 MaxSize=3,
 DesiredCapacity=2,
 AvailabilityZones= ['us-east-1a']
 )
 if str(response["ResponseMetadata"]["HTTPStatusCode"]) == "200":
 print("---- Creation of Auto Scaling Group using Launch Templates “)
 else:
 print("---- Creation of Auto Scaling Group using Launch Templates “)
 return True
# starting the execution from here
try:
 ec2_client = boto3.client('ec2')
 call_obj = CreateInstanceEC2(ec2_client)
 call_obj.create_ec2_auto_scaling_group()