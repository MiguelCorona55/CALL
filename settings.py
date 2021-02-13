from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
BASE_DIR
# system
AUDIO_DIR = BASE_DIR / 'audio'
ROLES_DIR = BASE_DIR / 'roles'

# S3
BUCKET_NAME_AUDIO = 'audio-input-data'
BUCKET_NAME_TRANSCRIPTIONS = 'transcription-output-data'
AUDIO_DIR_S3 = 'audio/'
TRANSCRIPTIONS_DIR = 'transcriptions/'
REGION = 'us-east-2'

if __name__ == '__main__':
    print('hola')
