import os

import settings
from aws_tools import s3

print('Starting process..')
# Upload audio files files
for entry in os.listdir(settings.AUDIO_DIR):
    path = os.path.join(settings.AUDIO_DIR, entry)
    if os.path.isfile(path):
        s3.upload_file(path, settings.BUCKET_NAME)
print('Process finished')
