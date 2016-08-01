import json
import boto3
from botocore.exceptions import ClientError

from chalice import NotFoundError
from chalice import Chalice

S3 = boto3.client('s3', region_name='ap-northeast-1')
BUCKET = 'YOUR_BUCKET_NAME'

app = Chalice(app_name='helloworld')


@app.route('/')
def index():
    return {'hello': 'world'}


@app.route('/hello/{name}')
def hello_name(name):
   # '/hello/james' -> {"hello": "james"}
   return {'hello': name}

@app.route('/objects/{key}', methods=['GET', 'POST'])
def s3objects(key):
    request = app.current_request
    if request.method == 'POST':
        S3.put_object(Bucket=BUCKET, Key=key,
                      Body=json.dumps(request.json_body))
    elif request.method == 'GET':
        try:
            response = S3.get_object(Bucket=BUCKET, Key=key)
            return json.loads(response['Body'].read())
        except ClientError as e:
            raise NotFoundError(key)
