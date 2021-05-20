import json
from datetime import datetime

import boto3
import pendulum
import pyarrow as pa
import pyarrow.parquet as pq
from botocore.exceptions import ClientError

from util.log import Log
from settings.aws_settings import AWSSettings


def lambda_handler(event: dict, context: dict) -> bool:

    log = Log.setup(name='logger')
    aws_settings = AWSSettings()

    timezone = pendulum.timezone('America/Sao_Paulo')
    date = datetime.now(tz=timezone).strftime('%Y-%m-%d')
    timestamp = datetime.now(tz=timezone).strftime('%Y%m%d%H%M%S')

    try:

        raw_key = event['Records'][0]['s3']['object']['key']
        raw_bucket = event['Records'][0]['s3']['bucket']['name']

        enriched_bucket = aws_settings.enriched_bucket

        client = boto3.client('s3')
        client.download_file(raw_bucket, raw_key, raw_key.split('/')[-1])

        with open(raw_key.split('/')[-1], mode='r', encoding='utf8') as fp:
            data = json.load(fp)

        parsed_data = dict()
        for key, value in data.items():
            if key == 'from' or key == 'chat':
                for k, v in data[key].items():
                    parsed_data[f"{key if key == 'chat' else 'user'}_{k}"] = [v]
            else:
                parsed_data[key] = [value]
        parsed_data['date'] = [date]
        parsed_data['timestamp'] = [timestamp]

        try:
            table = pa.Table.from_pydict(mapping=parsed_data)
            pq.write_table(table=table, where=f'./{timestamp}.parquet')
            client.upload_file(f"./{timestamp}.parquet", enriched_bucket, f"{date}/{timestamp}.parquet")
        except ClientError as exc:
            raise exc

        return True
    except Exception as exc:
        log.error(msg=exc)
        return False
