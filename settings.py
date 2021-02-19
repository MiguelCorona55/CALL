from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
# system
AUDIO_DIR = BASE_DIR / 'audio'
ROLES_DIR = BASE_DIR / 'roles'
LAMBDA_DIR = BASE_DIR / 'lambda_functions'

# S3
BUCKET_NAME_AUDIO = 'audio-input-data'
BUCKET_NAME_TRANSCRIPTIONS = 'transcription-output-data'
AUDIO_DIR_S3 = 'audio/'
TRANSCRIPTIONS_DIR = 'transcriptions/'
REGION = 'us-east-2'

# IAM
LAMBDA_ROLE_NAME = 'lambda-execute'

# Lambda
TRANSCRIBE_FUNC_NAME = 'transcribe_audio'
PARSE_FUNC_NAME = 'parse_transcription'
