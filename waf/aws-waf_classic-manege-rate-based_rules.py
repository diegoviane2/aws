#!/usr/bin/env python3
##############################################################################
# Description:                                                               #
# Set a new RATE LIMIT for a rate based WAF classic rule                     #
#                                                                            #
# Usage: aws-waf_classic-manege-rate-based_rules.py <RuleID> <RateLimit>     #  
#                                                                            #
# Written by Diego Viane Github: https://github.com/diegoviane2              #
##############################################################################

import boto3
import sys

# Retrive RULE ID from comand argument
Scope_RuleId = sys.argv[1]
rateLimit = sys.argv[2]
# Set Boto3 Client
client = boto3.client('waf')

# Describe rate based rules
def get_current_rule_data(ruleId):
    current = client.get_rate_based_rule(RuleId=ruleId)
    
    return current

# Get a Change token. Required on Update method
def request_change_token():
    token = client.get_change_token()

    return token

# Update the rate limit. Other informations are filled by current rule information
def update_rate_limit(ruleId, rateLim, changeToken, currentRuleData):

    currentNegated = currentRuleData['Rule']['MatchPredicates'][0]['Negated']
    currentType = currentRuleData['Rule']['MatchPredicates'][0]['Type']
    currentDataId = currentRuleData['Rule']['MatchPredicates'][0]['DataId']
    
    response = client.update_rate_based_rule(
        RuleId=ruleId,
        ChangeToken=changeToken,
        Updates=[{'Action':'INSERT','Predicate':{'Negated':currentNegated,'Type':currentType,'DataId':currentDataId}}],RateLimit=rateLim)

    print(response)

update_rate_limit(Scope_RuleId, rateLimit, request_change_token(), get_current_rule_data())
