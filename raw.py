import json
import gzip
import requests
from datetime import datetime

import pendulum
import boto3
from botocore.exceptions import ClientError

from util.log import Log
from settings.aws_settings import AWSSettings
from settings.telegram_settings import TelegramSettings


def lambda_handler(event: dict, context: dict) -> dict:

    log = Log.setup(name='logger')
    aws_settings = AWSSettings()
    telegram_settings = TelegramSettings()

    timezone = pendulum.timezone('America/Sao_Paulo')
    date = datetime.now(tz=timezone).strftime('%Y-%m-%d')
    timestamp = datetime.now(tz=timezone).strftime('%Y%m%d%H%M%S')

    try:

        token = telegram_settings.access_token
        base_url = f"https://api.telegram.org/bot{token}"
        data = json.loads(event["body"])
        chat_id = data["message"]["chat"]["id"]

        if chat_id == telegram_settings.chat_id:

            client = boto3.client('s3')
            bucket = aws_settings.raw_bucket
            root_path = aws_settings.root_path

            try:
                with open(f"{root_path}/{timestamp}.json", mode='w', encoding='utf8') as fp:
                    json.dump(data, fp)
                client.upload_file(f"{root_path}/{timestamp}.json", bucket, f"{date}/{timestamp}.json")
            except ClientError as exc:
                raise exc

        else:

            text = "I can't talk to strangers, sorry mate!"
            data = {"text": text, "chat_id": chat_id}
            data = gzip.compress(json.dumps(data).encode('utf-8'))
            headers = {'content-type': 'application/json', 'content-encoding': 'gzip'}
            url = base_url + "/sendMessage"
            requests.post(url=url, data=data, headers=headers)

    except Exception as exc:
        log.error(msg=exc)

    finally:
        return dict(statusCode="200")
