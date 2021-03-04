from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
# system
AUDIO_DIR = BASE_DIR / 'audio'
ROLES_DIR = BASE_DIR / 'roles'
LAMBDA_DIR = BASE_DIR / 'lambda_functions'

# S3
AUDIO_BUCKET_NAME = 'audio-input-data'
TRANSCRIPTIONS_BUCKET_NAME = 'transcription-output-data'
AUDIO_DIR_S3 = 'audio/'
TRANSCRIPTIONS_DIR = 'transcriptions/'
REGION = 'us-east-2'

# IAM
LAMBDA_ROLE_NAME = 'lambda-execute'

# Lambda
TRANSCRIBE_FUNC_NAME = 'transcribe_audio'
PARSE_FUNC_NAME = 'parse_transcription'
LANGUAGE_CODE = 'es-US'
