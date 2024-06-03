import os
from django.core.exceptions import ValidationError
def validate_audio_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.aac', '.midi', '.mpeg', '.mp3','.mp4', '.ogg', '.flac', '.wav', '.amr', 'aiff']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Extensión de archivo no válida')
    

def validate_video_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.3gp', '.mp4', '.m4v', '.mkv', '.webm', '.mov', '.avi', '.wmv', 'mpg', 'flv']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Extensión de archivo no válida')