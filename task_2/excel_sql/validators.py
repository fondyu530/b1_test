import os
from django.core.exceptions import ValidationError


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.xlsx', '.xls']
    if not ext.lower() in valid_extensions:
        raise ValidationError(f'Unsupported file extension. '
                              f'You can upload only {", ".join(valid_extensions)} extensions.')
