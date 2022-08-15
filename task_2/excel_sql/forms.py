from django.forms import forms
from .validators import validate_file_extension


class UploadFile(forms.Form):
    file = forms.FileField(validators=[validate_file_extension])
