#!/usr/bin/env python3
######################################################################################
# Description:                                                                       #
# This script clean the ECR repository for old outdated images                       #
# Before deletion, All kubernetes clusters are scanned for images that is running    #
# on pods and skips them.                                                            #
# This script delete images:                                                         #
# - Pushed at more than 15 days from the last pushed image                           #
# - With only 1 tag. Generally the latest and stable images have at least 2 tags     #
# - Images untagged                                                                  #
# This script Skip deletion of images:                                               #
# - With 2 or more tags. Could me latest or stable                                   #
# - Pushed at less than 15 days from the last pushed image                           #
# - Running on kubernetes cluster                                                    #
# The environment wich will run this script has to be confugured with kubectl remote #
# The environment wich will run this script has to be confugured with AWSCLI         #
# Written by Diego Viane Github: https://github.com/diegoviane2                      #
######################################################################################

from curses import keyname
from datetime import datetime, timedelta
import os
from re import T
import boto3
import sys
import csv
import operator

client = boto3.client('ecr')

running_images = []
ecr_filter = []
skip_count = 0
delete_count = 0
untagged = 0
total = 0
log = []

def del_images(imageDigest, registry_Id, repository_Name):
    image_Ids = []
    image_Ids.append({'imageDigest':imageDigest})
    
    #COMMENT SECTION FOR DEBBUG PURPOSES WITHOUT RUNNING ON SERVER
    
    ##########################
    # COMMENT THIS TO WORK #
    ##########################
    #response = []
    
    ##########################
    # UNCOMMENT THIS TO WORK #
    ##########################
    response = client.batch_delete_image(registryId=registry_Id, repositoryName=repository_Name, imageIds=image_Ids)

    return response

def kube_get_contexts():
    # Return an array containing all contexts from Kubernetes
    print("[ retrieving kubernetes contexts ]")
    result = []
    kube_cmd = "kubectl config get-contexts --no-headers | awk '{ print $2; }'"
    with os.popen(kube_cmd) as contexts:
        for line in contexts:
            result.append(line.strip())    
    return result

def kube_conext_ch(context):
    # change the current context on Kubernetes
    print("[ changing kubernetes context: " + context + "][ OK ]")
    kube_cmd = "kubectl config use-context " + context
    os.popen(kube_cmd).read().rstrip()
       
def kube_context_deployments(context):
    # Return an array containing all deployments from a context in Kubernetes
    # Changing kubernetes context
    kube_conext_ch(context)
    print("[ retrieving kubernetes deployments ]")
    result = []
    kube_cmd = "kubectl get deployments --no-headers | awk '{print $1}'"
    with os.popen(kube_cmd) as contexts:
        for line in contexts:
            result.append(line.strip())    
    return result

def kube_running_images():
    global running_images    
    for context in kube_get_contexts():
        for deployment in kube_context_deployments(context):   
            kube_cmd = "kubectl get deploy "+ deployment +" -o=jsonpath='{$.spec.template.spec.containers[:1].image}' | cut -d ':' -f 2"
            #print("[ retrieving kubernetes running images ]")
            with os.popen(kube_cmd) as contexts:
                for line in contexts:
                    running_images.append(line.strip())

def get_repositories():
    result = []
    repositories = client.describe_repositories(maxResults=1000)
    for repository in repositories['repositories']:
        result.append({"repositoryName":repository['repositoryName']})
        
    return result

def ecr_delete_tagged_images():
    global ecr_filter
    global skip_count
    global delete_count
    global total
    kube_running_images()
    print("[ filtering ecr images ]")
    dataset = []
    for repository in get_repositories():
        repoName = repository['repositoryName']
        
        dataset = client.describe_images(repositoryName=repoName,filter={'tagStatus': 'TAGGED'}, maxResults=1000)
       
        if len(dataset['imageDetails']) != 0:
            total = total + len(dataset['imageDetails'])
            target_date = max(dataset['imageDetails'], key=lambda x:x['imagePushedAt'],default={'imagePushedAt':datetime.now()})
            target_date = target_date['imagePushedAt']
            
            target_date =  target_date + timedelta(days = -15)
            
            
            for item in dataset['imageDetails']:
              
                # Skip Image with more than 2 tags. Generally Latest or Stable images have 2 tags ['#commit_tag','latest/stable']
                # Skip Image in grace period
                # Skip Image running in Kubernetes                                       
                if len(item['imageTags']) < 2:
                    if item['imagePushedAt'] < target_date:
                        count = 0
                        for run in running_images:
                            if run == item['imageTags'][0]:
                                print('[ skipping running images ] [INFO]')
                                count+=1
                                skip_count+=1
                        if count == 0:    
                            imageDigest = item['imageDigest']
                            registryId = item['registryId']
                            repositoryName = item['repositoryName']
                            print(del_images(imageDigest, registryId, repositoryName))
                            delete_count+=1
                else:
                    skip_count+=1
                                    
def ecr_delete_untagged_images():
    global untagged
    print('[ deleting [UNTAGGED] images ... ][ INFO ]')
    for repository in get_repositories():
        repoName = repository['repositoryName']
        dataset = client.describe_images(repositoryName=repoName,filter={'tagStatus': 'UNTAGGED'}, maxResults=1000)
        dl_cn = 0
        if len(dataset['imageDetails']) != 0:
            for item in dataset['imageDetails']:
                         
                imageDigest = item['imageDigest']
                registryId = item['registryId']
                repositoryName = item['repositoryName']
                print(del_images(imageDigest, registryId, repositoryName))
                untagged+=1
                   
        
ecr_delete_tagged_images()
ecr_delete_untagged_images()
log.append({"skipped":skip_count, "deleted":delete_count, "untagged":untagged})


print("TOTAL No. of IMAGES: " + str(total))
print("SKIPPED IMAGES: " + str(log[0]['skipped']) + " [ skipped ]")
print("DELETED IMAGES: " + str(log[0]['deleted']) + " [ deleted ]")
print("UNTAGGED IMAGES: " + str(log[0]['untagged']) + " [ deleted ]")
