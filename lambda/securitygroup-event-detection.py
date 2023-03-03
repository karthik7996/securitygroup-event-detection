import logging
import json
import os
import boto3
import urllib3

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

slack_url = os.environ['slack_url']
teams_url = os.environ['teams_url']


def lambda_handler(event, context):
    print("@@@@@@@@@@@@@")
    print(event)
    global sgid
    setup_logging()
    account_id = event['account']
    event_name = event['detail']['eventName']
    region = event['region']
    principalId = event['detail']['userIdentity']['principalId']
    user = principalId.split(":")[-1]
    Arn = event['detail']['userIdentity']['arn']
    Role =Arn.split("/")[-2]
    if event_name == "DeleteSecurityGroup":
        sgdid = event['detail']['requestParameters']
        for i,j in sgdid.items():
            if i == "groupId":
                sg_idd = j
                print(sg_idd)
        message = "Security Group alert. \n" "Incident: " + event_name + "\n"  + "Account: " + account_id +  "\n" + 'SG ID: ' + str(sg_idd) + "\n" + 'User: ' + str(user) + "\n" + 'Region: ' + str(region)+ '\n'  + "Role: " + Role 
    elif event_name == "AuthorizeSecurityGroupIngress":
        sg_id = event['detail']['requestParameters']
        for i,j in sg_id.items():
                if i == "groupId":
                    sgid = j
                    print("@@@@@")
                    print(sgid)
        a = event['detail']['requestParameters']['ipPermissions']['items']
        for i,j in a[0].items():
            if i == "fromPort":
                y=j
                print(y)
            elif i == "toPort":
                x=j
                print(x)
            elif i == "ipRanges":
                for m,n in j.items():
                    if m == "items":
                        for k,p in n[0].items():
                            if k=="cidrIp":
                                z=p
                                print(p)
        message = "Security Group alert. \n" "Incident: " + event_name + "\n"  + "Account: " + account_id +  "\n" + 'SG ID: ' + str(sgid) + "\n" + 'User: ' + str(user) + "\n" + 'Region: ' + str(region)+ '\n'  + "Role: " + Role + "\n" + "FromPort:" + str(y)+'\n'+"Toport:"+str(x) + "\n"+ 'Cidr_range:' +str(z)
    elif event_name == "RevokeSecurityGroupIngress":
        sg_id = event['detail']['requestParameters']
        for i,j in sg_id.items():
            if i == "groupId":
                sgid = j
                print(sgid)
        message = "Security Group alert. \n" "Incident: " + event_name + "\n"  + "Account: " + account_id +  "\n" + 'SG ID: ' + str(sgid) + "\n" + 'User: ' + str(user) + "\n" + 'Region: ' + str(region)+ '\n'  + "Role: " + Role 
            
    else:
        sg_id = event['detail']['responseElements']
        for i,j in sg_id.items():
            if i == "groupId":
                sgid = j
                print("@@@@@")
                print(sgid)
                
        message = "Security Group alert. \n" "Incident: " + event_name + "\n"  + "Account: " + account_id +  "\n" + 'SG ID: ' + str(sgid) + "\n" + 'User: ' + str(user) + "\n" + 'Region: ' + str(region)+ '\n'  + "Role: " + Role 
    post_to_slack(message)
    print("&&&&&&&&&&&&&")
    print(message)
    
def post_to_slack(message):
    webhook_url = slack_url
    log.info(str(webhook_url))
    teams_webhook_url = teams_url
    log.info(str(teams_webhook_url))
    slack_data = {'text': message}
    http = urllib3.PoolManager()
    headers={'Content-Type': 'application/json'}
    encoded_data = json.dumps(slack_data).encode('utf-8')
    response = http.request('POST',webhook_url,body=encoded_data,headers=headers)
    log.info('response is :'+str(response))
    response1 = http.request('POST',teams_webhook_url,body=encoded_data,headers=headers)
    log.info('response-1 is :'+str(response1))
    return True
    
def setup_logging():
    """
    Logging Function.
    Creates a global log object and sets its level.
    """
    global log
    log = logging.getLogger()
    log_levels = {'INFO': 20, 'WARNING': 30, 'ERROR': 40}

    if 'logging_level' in os.environ:
        log_level = os.environ['logging_level'].upper()
        if log_level in log_levels:
            log.setLevel(log_levels[log_level])
        else:
            log.setLevel(log_levels['ERROR'])
            log.error("The logging_level environment variable is not set to INFO, WARNING, or \
                    ERROR.  The log level is set to ERROR")
    else:
        log.setLevel(log_levels['ERROR'])
        log.warning('The logging_level environment variable is not set. The log level is set to \
                  ERROR')
        #log.info('Logging setup complete - set to log level ' + log_level)