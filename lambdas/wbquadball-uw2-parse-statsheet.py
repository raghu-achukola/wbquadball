import json
# Inc 6 -> test if lambda function can access quadball package in layer
from quadball.statsheet.parser import gen_statsheet_possessions

def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Custom code')
    }
