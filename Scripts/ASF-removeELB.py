import boto3
import json

def script_handler(event, context):
  elb_client = boto3.client('elb')
  var_familia = event.get('elbgroup')
  var_ec2 = event.get('instanceid')
  out= {}
  response_elb = elb_client.describe_load_balancers()
  for elb in response_elb['LoadBalancerDescriptions']:
    elb_name = elb['LoadBalancerName']
    response_elb_name= elb_client.describe_tags(LoadBalancerNames=[elb_name])
    for tag in response_elb_name['TagDescriptions']:
      elb_name = tag['LoadBalancerName']
      for tagname in tag['Tags']:
        if tagname['Key'] == 'ELBGROUP' and tagname['Value'] == var_familia:
          response_remove_elb = elb_client.deregister_instances_from_load_balancer(LoadBalancerName=elb_name,Instances=[{'InstanceId': var_ec2}])
          out = {"Response": response_remove_elb}
          
  return out