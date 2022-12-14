import os
from django.core.exceptions import ValidationError
from .models import UploadedFile


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.xlsx', '.xls']
    if not ext.lower() in valid_extensions:
        raise ValidationError(f'Unsupported file extension. '
                              f'You can upload only {", ".join(valid_extensions)} extensions.')


def validate_existing_files(value):
    file_name = value.name
    try:
        UploadedFile.objects.get(name=file_name)
        raise ValidationError(f"File with name '{file_name}' already exists in DB. Rename this file.")
    except UploadedFile.DoesNotExist:
        pass
