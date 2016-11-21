# coding: utf-8
from __future__ import unicode_literals

import uuid

from . import s3_client, bucket_name


def _get_image_url(filename):
    return s3_client.generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': bucket_name, 'Key': filename})


def upload_to_s3(message_content):
    file_name = str(uuid.uuid4()) + '.jpg'
    file_path = '/tmp/{}'.format(file_name)
    with open(file_path, 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)

    s3_client.upload_file(file_path, bucket_name, file_name)
    return _get_image_url(file_name)
