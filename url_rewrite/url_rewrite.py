import json
import re


def lambda_handler(event, context):
    try:
        request = event['Records'][0]['cf']['request']
        print('initial request uri: {}'.format(request['uri']))

        if request['uri'].endswith('/') and not re.search(r'\.', request['uri']):
            request['uri'] = '{}{}'.format(request['uri'], 'index.html')
            print('rewritten uri: {}'.format(request['uri']))
        elif re.search(r'\.', request['uri']) and not request['uri'].endswith('/'):
            request['uri'] = request['uri']
            print('url contains ".", therefore not rewritten')
        elif not request['uri'].endswith('/') and not re.search(r'\.', request['uri']):
            request['uri'] = '{}{}'.format(request['uri'], '/index.html')
            print('url does not contain ".", nor "/", therefore rewritten')
        else:
            print("no rewrite")
            pass
        print('final request uri: {}'.format(request['uri']))
        return request

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({
                'uri': request['uri'],
                'message': 'malformed uri or object does not exist'
            }),
        }
