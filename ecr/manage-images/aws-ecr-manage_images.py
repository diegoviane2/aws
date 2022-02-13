#!/usr/bin/env python3

import boto3
client = boto3.client('ecr')
def get_repositories():
    result = []
    repositories = client.describe_repositories()
    for repository in repositories['repositories']:
        result.append({"repositoryName":repository['repositoryName']})
    return result
def get_images_info():
    dataset = []
    result=[]
    for repository in get_repositories():
        repoName = repository['repositoryName']
        dataset = client.describe_images(repositoryName=repoName)
        for item in dataset['imageDetails']:
            result.append({'repositoryName':item['repositoryName'],'imagePushedAt':item['imagePushedAt'].strftime('%d/%m/%Y')})
    return result


print(get_images_info())