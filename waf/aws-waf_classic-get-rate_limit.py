#!/usr/bin/env python3
##############################################################################
# Description:                                                               #
# Get the current RATE LIMIT for a rate based WAF classic rule               #
#                                                                            #
# Written by Diego Viane Github: https://github.com/diegoviane2              #
##############################################################################

import boto3

def get_current_rate_limit(ruleId):
    response = client.get_rate_based_rule(RuleId=ruleId)
    
    current = response['Rule']['RateLimit']

    return current

print(get_current_rate_limit())
