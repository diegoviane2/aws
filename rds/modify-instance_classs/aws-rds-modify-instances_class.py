#!/usr/bin/env python3
##############################################################################
# Description:                                                               #
# Get All Instances from RDS in a REGION and modify INSTANCE CLASS atribute  #
# to the desired instance class on a CSV file.                               #
# The script could be executed on a scheduled pipeline and prevent instances #
# to be out of configuration.                                                #
# The environment wich will run this script has to be confugured with AWSCLI #
# Written by Diego Viane Github: https://github.com/diegoviane2              #
##############################################################################
import boto3
import csv
import sys
from datetime import datetime

client = boto3.client('rds')

def get_instances_info():
    result = []
    instances = client.describe_db_instances()
    for instance in instances['DBInstances']:
        result.append({"DBInstanceIdentifier":instance['DBInstanceIdentifier'] , "DBInstanceClass":instance['DBInstanceClass']})
    return result

def modify_instances(apply_imediately):
    for instance in get_instances_info():
        identifier = instance['DBInstanceIdentifier']
        instance_class = instance['DBInstanceClass']
        with open('desired_db_classes.csv') as classes:
            dataset = csv.reader(classes, delimiter=',')
            for lines in dataset:
                desired_identifier = lines[0]
                desired_instance_class = lines[1]
                if desired_identifier == identifier:
                    if desired_instance_class == instance_class:
                        print(' [ Instance ' + identifier + ' has the desired >>' + instance_class + '<< class ... ] [ OK ]')
                    else:
                        print(' [ Setting instance modifications ' + identifier + ': from ' + instance_class + ' to ' + desired_instance_class + ']')
                        if apply_imediately:
                            result = client.modify_db_instance(DBInstanceIdentifier=identifier,DBInstanceClass = desired_instance_class,ApplyImediately=apply_imediately)
                            print(' [ Applying modifications IMEDIATELLY ... ] [ OK ]')
                            ##########################
                            # UNCOMMENT THIS TO WORK #
                            ##########################
                            print(result)
                        else:
                            result =  client.modify_db_instance(DBInstanceIdentifier=identifier,DBInstanceClass = desired_instance_class,ApplyImediately=apply_imediately)
                            print(' [ Scheduling instance modifications ... ] [ OK ]')
                            ##########################
                            # UNCOMMENT THIS TO WORK #
                            ##########################
                            print(result)

def check_launch_periods():
    ###################################################
    # Return TRUE if TODAY is in a Launch Period      #
    # Return FALSE if TODAY is NOT in a Launch Period #
    ###################################################
    today = datetime.today().strftime('%d/%m/%Y %H:%M')
    with open('launch_period.csv') as classes:
        dataset = csv.reader(classes, delimiter=',')
        for line in dataset:
            if today >= line[0] and today <= line[1]:
                return True
    return False

args = sys.argv[1]

if check_launch_periods():
    print(' [ Script checking if TODAY is in a LAUNCH PRODUCT PERIOD ... ] ')    
    print(' [ Script execution stopped. REASON: TODAY is in a LAUNCH PRODUCT PERIOD ... ] [ FAILED ]')
else:
    print(' [ Script checking if TODAY is in a LAUNCH PRODUCT PERIOD ... ] ')
    print(' [ Script execution started. TODAY is NOT in a LAUNCH PRODUCT PERIOD ... ]')
    if args == 'now':
        modify_instances(True)
    else:
        modify_instances(False)
