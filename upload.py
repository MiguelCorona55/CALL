import os

import settings
from aws_tools import s3

print('Starting process..')
# Upload audio files files
for entry in settings.AUDIO_DIR.iterdir():
    if entry.is_file():
        s3.upload_file(entry, settings.AUDIO_BUCKET_NAME)
print('Process finished')
